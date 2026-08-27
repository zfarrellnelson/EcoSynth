import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', 5000)) # Listens on all interfaces at port 5000, not a specific ip from the sender
s.listen(1)
conn, addr = s.accept()
print(f"Connected by {addr}")
print(conn.recv(1024).decode()) # Prints the received message, not just a recieved message
conn.close()
