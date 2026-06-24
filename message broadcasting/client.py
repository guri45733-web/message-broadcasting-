import socket
import threading
import json
import tkinter as tk
from tkinter import ttk, messagebox

server_socket = None

def append_message(text):
    chat_box.config(state="normal")
    chat_box.insert("end", text + "\n")
    chat_box.see("end")
    chat_box.config(state="disabled")

def listen_to_server(sock):
    try:
        file = sock.makefile("r", encoding="utf-8")
        while True:
            line = file.readline()
            if not line:
                break
            msg = json.loads(line.strip())
            if msg.get("type") == "announcement":
                append_message(f"[{msg.get('time','--:--:--')}] {msg.get('message','')}")
            elif msg.get("type") == "auth_result":
                if msg.get("status") == "ok":
                    append_message("Connected successfully.")
                else:
                    append_message("Access denied. Wrong password.")
                    messagebox.showerror("Connection failed", "Wrong password.")
                    break
    except:
        append_message("Disconnected from server.")
    finally:
        try:
            sock.close()
        except:
            pass

def connect_to_server():
    global server_socket
    host = ip_entry.get().strip()
    password = password_entry.get().strip()
    if not host or not password:
        messagebox.showwarning("Missing info", "Enter server IP and password.")
        return

    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect((host, 5050))

        auth_data = {"type": "auth", "password": password}
        server_socket.sendall((json.dumps(auth_data) + "\n").encode("utf-8"))
        threading.Thread(target=listen_to_server, args=(server_socket,), daemon=True).start()
        connect_btn.config(state="disabled")
        append_message(f"Connecting to {host}:5050 ...")
    except Exception as e:
        messagebox.showerror("Connection error", str(e))

root = tk.Tk()
root.title("Private Network Announcement Client")
root.geometry("650x450")

top = ttk.Frame(root, padding=10)
top.pack(fill="x")

ttk.Label(top, text="Server IP:").grid(row=0, column=0, sticky="w")
ip_entry = ttk.Entry(top, width=25)
ip_entry.grid(row=0, column=1, padx=8)
ip_entry.insert(0, "192.168.1.1")

ttk.Label(top, text="Password:").grid(row=1, column=0, sticky="w", pady=5)
password_entry = ttk.Entry(top, width=25, show="*")
password_entry.grid(row=1, column=1, padx=8, pady=5)

connect_btn = ttk.Button(top, text="Connect", command=connect_to_server)
connect_btn.grid(row=0, column=2, rowspan=2, padx=8)

mid = ttk.Frame(root, padding=10)
mid.pack(fill="both", expand=True)

ttk.Label(mid, text="Messages:").pack(anchor="w")
chat_box = tk.Text(mid, state="disabled")
chat_box.pack(fill="both", expand=True, pady=5)

root.mainloop()