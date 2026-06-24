# Private Network Announcement System (Python)

This project lets an **admin** send announcements over a **local network (hotspot or Wi‑Fi)** to multiple **read‑only clients**.  
Only the admin can send messages, and all connected users can see the announcements in real time.

---

## Features

- Admin server broadcasts announcements to all connected clients.
- Clients can only receive and view messages, not send.
- Works over any local network (mobile hotspot, Wi‑Fi router, etc.).
- Simple GUI for both server and clients using Tkinter.
- Password-based access so only users with the password can connect.

---

## Project Structure

- `server.py` – Admin application, starts the server and sends announcements.
- `client.py` – User application, connects to server and shows announcements.
- `README.md` – This documentation file.
- `requirements.txt` – List of Python dependencies (standard library only, so it is empty).

---

## Requirements

- Python 3.8 or later installed.
- OS: Windows / Linux / macOS (Tkinter must be available; it ships with most Python installers).
- All devices connected to the **same local network** (same Wi‑Fi or hotspot).

No third‑party libraries are required; only Python’s built‑in modules are used:
- `socket`, `threading`, `json`, `datetime`
- `tkinter`, `tkinter.ttk`, `tkinter.messagebox`

---

## How It Works

- The admin runs `server.py` on a laptop/PC that is hosting or connected to the Wi‑Fi/hotspot.
- The server listens on port `5050` on all network interfaces (`0.0.0.0`) and waits for client connections.
- Each client runs `client.py`, enters:
  - the server’s IP address on the local network,
  - the shared admin password.
- After successful authentication, clients receive all future announcements broadcast by the admin.

---

## Setup and Running (Admin / Server)

1. Open the project folder in **VS Code**.
2. Make sure Python is selected as the interpreter.
3. Run the admin server:
   ```bash
   python server.py
   ```
4. In the GUI:
   - Optionally change the admin password and click **Set Password**.
   - Click **Start Server**.
5. Find your machine’s local IP address (examples):
   - On Windows: `ipconfig` in Command Prompt, look for IPv4 address.
   - On Linux/macOS: `ifconfig` or `ip addr`, look for your active network interface.
6. Share this IP address and password with all users who will run the client.

---

## Setup and Running (Client / User)

1. Copy the project folder or just `client.py` to the client device.
2. Make sure Python 3 is installed on that device.
3. Run:
   ```bash
   python client.py
   ```
4. In the client GUI:
   - Enter the **Server IP** (the admin’s machine IP on the same network).
   - Enter the **Password** (must match the admin password).
   - Click **Connect**.
5. Once connected, the client will show:
   - Connection status messages.
   - All subsequent announcements sent by the admin.

---

## Sending Announcements (Admin)

1. In the server window (`server.py`):
   - Type the announcement text in the **Announcement to send** box.
   - Click **Send Announcement**.
2. The announcement is instantly broadcast to all connected clients.
3. Each client sees the message with a timestamp in their **Messages** area.

---

## Changing the Admin Password

- Default password: `admin123`.
- In the server GUI:
  1. Enter a new password in the **Admin password** field.
  2. Click **Set Password**.
- All clients must use this same password when connecting.

---

## Notes and Limitations

- This system is designed for **local/private networks only**, not the public internet.
- All devices (server + clients) **must be on the same network**:
  - Same Wi‑Fi router, or
  - Same mobile hotspot.
- Firewalls:
  - On Windows or other OSes, you may need to allow Python or port 5050 for private networks.
- Security:
  - Password is sent in plain text over the local network.
  - Suitable for small, trusted environments (classroom, office room, home).
  - For production or sensitive use, you should add:
    - Encryption (e.g., TLS),
    - Stronger authentication and user management.

---

## Customization Ideas

You can extend this project with:
- Persistent message log (save announcements to a file or database).
- Client list display (show which clients are connected).
- Different channels/topics (e.g., General, Urgent, Alerts).
- Sound notifications on client when a new announcement arrives.
- Better UI design with themes or a web-based front‑end (Flask + web sockets).

---

## Troubleshooting

- **Client cannot connect**:
  - Check that the server is running and the port is not blocked by firewall.
  - Confirm that IP address and password are correct.
  - Ensure both devices are on the same Wi‑Fi/hotspot network.
- **No messages received**:
  - Confirm the client shows “Connected successfully.”
  - Make sure you click **Send Announcement** after typing the message.
- **Tkinter not found**:
  - On some Linux distributions, you might need to install Tkinter separately (e.g., `sudo apt install python3-tk`).

---

## License

This project is free for personal and educational use.  
You can modify and extend it as you like for your own purposes.