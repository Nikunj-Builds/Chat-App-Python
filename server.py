import socket
import threading

HOST = "0.0.0.0"     # Listen on all network interfaces
PORT = 8090          # Must match PORT in main.py

clients = []         # All connected clients


def handle(conn):
    while True:
        try:
            data = conn.recv(1024)
        except OSError:
            break
        if not data:
            break
        print("received:", data.decode(), flush=True)
        # Send what arrived to everyone else (not the sender)
        for other in clients:
            if other is not conn:
                try:
                    other.sendall(data)
                except OSError:
                    pass
    if conn in clients:
        clients.remove(conn)
    conn.close()


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(5)
print(f"server running on {HOST}:{PORT}...", flush=True)

while True:
    conn, addr = s.accept()
    print("client connected:", addr, flush=True)
    clients.append(conn)
    threading.Thread(target=handle, args=(conn,), daemon=True).start()
