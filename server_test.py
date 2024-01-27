import requests
from threading import Thread
from server import HttpConnectionListener 

def create_server():
  server = HttpConnectionListener()
  server.listen()
  thread = Thread(target = server.run_event_loop, args=())
  thread.start()
  return (server, thread)

def test_httpget():
  server, _ = create_server()
  response = requests.get("http://127.0.0.1:8080")
  assert response.status_code == 200
  server.stop
  
