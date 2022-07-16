import socket, random
from threading import Thread

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clients = []

ip_address = '127.0.0.1'
port = 8000
server.bind((ip_address, port))
server.listen()

questions = [
  ["What is Cynophobia the fear of?\n a) Dogs\n b) Crowded Areas\n c) Heights", "a"],
  ["Where is the headquarters of the IAEA?\n a) Vienna\n b) Argentina\n c) Brazil", "a"],
  ["What was former President William Taft's pet cow?\n a) Pauline\n b) Bessie\n c) Daisy", "a"],
  ["The quote \"What, you egg?\" is from which Shakespearean play?\n a) Macbeth\n b) The Tempest\n c) King Lear", "a"],
  ["What is the boiling point of ethanol?\n a) 87.4℃\n b) 78.4℃\n c) 47.8℃", "b"],
  ["Which of these is not a color of the Olympic Rings?\n a) Blue\n b) Orange\n c) Black", "b"],
  ["What was the name of Alexander the Great's horse?\n a) Cassius\n b) Bucephalus\n c) Fabius", "b"],
  ["Napolean suffered defeat at Waterloo in what year?\n a) 1769\n b) 1815\n c) 1812", "b"],
  ["When did the Second World War end?\n a) 1939\n b) 1918\n c) 1945", "c"],
  ["How many points is the letter\"K\" in the game Scrabble?\n a) 2\n b) 8\n c) 5", "c"],
  ["Which of these people is depicted on the US $100 bill?\n a) FDR\n b) Obama\n c) Benjamin Franklin", "c"]
]

def remove_qna(qna):
  if qna in questions:
    questions.remove(qna)

def get_qna(conn):
  qna = random.choice(questions)
  conn.send(qna[0])
  return qna

def clientthread(conn, addr):
  score = 0
  conn.send("Welcome to the quiz game!".encode("utf-8"))
  conn.send("Guess the correct answer out of three options. Good luck!\n\n".encode("utf-8"))

  while len(questions) > 0:
    qna = get_qna(conn)
    try:
      msg = conn.recv(2048).decode("utf-8")
      if msg:
        if msg == qna[1]:
          score +=1
          conn.send("Amazing! Your score is {score}. Keep going!\n\n")
        else:
          conn.send("Whoops! That wasn't the right answer! Your score is {score}.\n\n")
        remove_qna(qna)
      else:
        if conn in clients: 
          clients.remove(conn)
    except:
      continue

while True:
  conn, addr = server.accept()
  clients.append(conn)
  print(addr[0] + "connected")

  new_thread = Thread(target=clientthread, args=(conn, addr))
  new_thread.start()