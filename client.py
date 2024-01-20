import socket
from server import HttpConnectionListener 

class HttpConnection():
  def __init__(self):
    self.HOST = "127.0.0.1"
    self.PORT = 65432

  def send(self): 
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
      s.connect((self.HOST,self.PORT))
      s.sendall(b"Hello, world")
      data = s.recv(1024)
      print(f"Recieved back {data}")

HttpConnection().send()
