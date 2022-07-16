import socket
from threading import Thread

username = input("Enter your name: ")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = '127.0.0.1'
port = 8000

client.connect((ip_address, port))
print("Connected with the server")

def receive():
  while True:
    try:
      msg = client.recv(2048).decode('utf-8')
      if msg == '__USERNAME__':
        client.send(username.encode('utf-8'))
      else:
        print(msg)
    except:
      print("An error occurred. Try connecting again.")
      client.close()
      break

def write():
  while True:
    client.send(input().encode("utf-8"))
    
rcv_thread = Thread(target = receive)
wrt_thread = Thread(target = write)
rcv_thread.start()
wrt_thread.start()