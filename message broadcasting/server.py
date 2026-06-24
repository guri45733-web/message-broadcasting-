import socket
import threading
import json
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

HOST = "0.0.0.0"
PORT = 5050
ADMIN_PASSWORD = "admin123"

clients = []
client_lock = threading.Lock()

def log(text):
    timestamp = datetime.now().strftime("%H:%M:%S")
    log_box.config(state="normal")
    log_box.insert("end", f"[{timestamp}] {text}\n")
    log_box.see("end")
    log_box.config(state="disabled")

def broadcast(message_dict):
    data = (json.dumps(message_dict) + "\n").encode("utf-8")
    with client_lock:
        for client in clients[:]:
            try:
                client.sendall(data)
            except:
                try:
                    clients.remove(client)
                except:
                    pass

def handle_client(conn, addr):
    try:
        file = conn.makefile("r", encoding="utf-8")
        first = file.readline().strip()
        if not first:
            conn.close()
            return

        auth = json.loads(first)
        if auth.get("type") != "auth" or auth.get("password") != ADMIN_PASSWORD:
            conn.sendall((json.dumps({"type": "auth_result", "status": "denied"}) + "\n").encode("utf-8"))
            conn.close()
            log(f"Rejected connection from {addr[0]}:{addr[1]}")
            return

        conn.sendall((json.dumps({"type": "auth_result", "status": "ok"}) + "\n").encode("utf-8"))
        with client_lock:
            clients.append(conn)
        log(f"Client connected: {addr[0]}:{addr[1]}")

        while True:
            data = file.readline()
            if not data:
                break
    except:
        pass
    finally:
        with client_lock:
            if conn in clients:
                clients.remove(conn)
        try:
            conn.close()
        except:
            pass
        log(f"Client disconnected: {addr[0]}:{addr[1]}")

def accept_connections(server_socket):
    while True:
        conn, addr = server_socket.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

def start_server():
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        log(f"Server started on port {PORT}")
        log("Share your PC hotspot/Wi-Fi IP with clients, then run client.py on their devices.")
        threading.Thread(target=accept_connections, args=(server_socket,), daemon=True).start()
        start_btn.config(state="disabled")
    except Exception as e:
        messagebox.showerror("Server Error", str(e))

def send_announcement():
    msg = message_entry.get("1.0", "end").strip()
    if not msg:
        return
    message_dict = {
        "type": "announcement",
        "message": msg,
        "time": datetime.now().strftime("%H:%M:%S")
    }
    broadcast(message_dict)
    log(f"Admin: {msg}")
    message_entry.delete("1.0", "end")

root = tk.Tk()
root.title("Private Network Announcement Server")
root.geometry("700x500")

top = ttk.Frame(root, padding=10)
top.pack(fill="x")

ttk.Label(top, text="Admin password:").grid(row=0, column=0, sticky="w")
password_var = tk.StringVar(value=ADMIN_PASSWORD)
password_entry = ttk.Entry(top, textvariable=password_var, show="*", width=30)
password_entry.grid(row=0, column=1, padx=8)

def update_password():
    global ADMIN_PASSWORD
    ADMIN_PASSWORD = password_var.get().strip()
    if not ADMIN_PASSWORD:
        messagebox.showwarning("Warning", "Password cannot be empty.")
        password_var.set("admin123")
        ADMIN_PASSWORD = "admin123"

ttk.Button(top, text="Set Password", command=update_password).grid(row=0, column=2, padx=5)
start_btn = ttk.Button(top, text="Start Server", command=start_server)
start_btn.grid(row=0, column=3, padx=5)

mid = ttk.Frame(root, padding=10)
mid.pack(fill="both", expand=True)

ttk.Label(mid, text="Announcement to send:").pack(anchor="w")
message_entry = tk.Text(mid, height=4)
message_entry.pack(fill="x", pady=5)

ttk.Button(mid, text="Send Announcement", command=send_announcement).pack(anchor="e", pady=5)

ttk.Label(mid, text="Server log:").pack(anchor="w", pady=(10, 0))
log_box = tk.Text(mid, height=15, state="disabled")
log_box.pack(fill="both", expand=True, pady=5)

root.mainloop()