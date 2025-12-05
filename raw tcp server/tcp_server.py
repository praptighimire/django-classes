import socket

HOST = "0.0.0.0"
PORT = 9091
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen()
print(f"TCP server running on port {PORT}")

while True:
    client_socket, client_addr = server_socket.accept()
    print(f"Connection from {client_addr}")

    data = client_socket.recv(1024)
    if not data:
        client_socket.close()
        continue
    print(f"Received: {data.decode(errors='ignore')}")
    client_socket.send(b"Message received")
    client_socket.close()
