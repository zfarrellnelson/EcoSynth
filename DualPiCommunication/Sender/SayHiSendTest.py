import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('192.168.2.64', 5000)) # replace with pi4 ip if it changes
s.sendall(b'Hello from the sender Pi!')
s.close()
