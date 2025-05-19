import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('0.0.0.0', 9999))

client.send("Hello from Client".encode())
print(client.recv(1024).decode())