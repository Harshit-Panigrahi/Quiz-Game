import socket, random
from threading import Thread

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clients = []

ip_address = '10.0.0.1'
port = 8000
server.bind((ip_address, port))
server.listen()

questions = [
  ["What is the boiling point of ethanol?\n a) 87.4℃\n b) 78.4℃\n c) 47.8℃", "b"],
  ["When did the Second World War end?\n a) 1939\n b) 1918\n c) 1945", "c"],
  ["Where is the headquarters of the IAEA?\n a) Vienna\n b) Argentina\n c) Brazil", "a"],
  ["Which of these is not a color of the Olympic Rings?\n a) Blue\n b) Orange\n c) Black", "b"],
]

def clientthread(conn, addr):
  score = 0
  conn.send("Welcome to the quiz game!".encode("utf-8"))
  conn.send("Guess the correct answer out of three options. Good luck!\n\n".encode("utf-8"))

  while True:
    qna = random.choice(questions)
    try:
      msg = conn.recv(2048).decode("utf-8")
      if msg:
        if msg.lower == qna[1]:
          score +=1
          conn.send("Amazing! Your score is {score}. Keep going!\n\n")
        else:
          conn.send("Whoops! That wasn't the right answer. Your score is {score}.\n\n")
        questions.remove(qna)
    except:
      continue

while True:
  conn, addr = server.accept()
  clients.append(conn)
  print(addr[0] + "connected")

  new_thread = Thread(target=clientthread, args=(conn, addr))
  new_thread.start()