import socket
import selectors
import types

class HttpConnectionListener:
  def __init__(self, host, port):
    self.host = host 
    self.port = port
    self.sel = selectors.DefaultSelector()
    self.running = False 

  def accept_wrapper(self, sock):
    conn, addr = sock.accept()
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    self.sel.register(conn, events, data=data)

  def service_connection(self, key, mask):
    sock = key.fileobj
    data = key.data 
    if mask & selectors.EVENT_READ:
      recv_data = sock.recv(1024)
      if recv_data:
        data.outb += b"HTTP/1.1 200 OK\r\ncontent-length: 0\r\n\r\n" 
      else:
        print(f"Closing connection to {data.addr}")
        self.sel.unregister(sock)
        sock.close()
    if mask & selectors.EVENT_WRITE:
      if data.outb:
        sent = sock.send(data.outb)
        data.outb = data.outb[sent:]

  def listen(self): 
    lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    lsock.bind((self.host, self.port))
    lsock.listen() 
    lsock.setblocking(False)
    self.sel.register(lsock, selectors.EVENT_READ, data=None)

  def run_event_loop(self):
    self.running = True
    try:
      while self.running:
        events = self.sel.select(timeout=None)
        for key, mask in events:
          if key.data is None:
            self.accept_wrapper(key.fileobj)
          else:
            self.service_connection(key, mask)
    except KeyboardInterrupt:
      print("Caught keyboard interrupt, exiting")
    finally:
      self.sel.close()

  def stop(self):
    self.running = False
