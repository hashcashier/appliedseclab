import socket
import sys
from os.path import exists

#check number of arguments
if len(sys.argv) < 2:
  print "Usage : python log_client <filename>"
  sys.exit()

buf = 1024
myName = "Sender" #TODO CA or WS depending on the case
filename = sys.argv[1]

#check if file exists
if not exists(filename):
  print "File not found"
  sys.exit()

#read from file
fd = open(filename, "r") #TODO read bytes? depends on what file
myFile = fd.read()
fd.close()

#encrypt, hash
encrypted = myFile#TODO encrypt contents of "myfile" with AES?
myHash = encrypted #TODO hash(encrypted)) 
mySign = "Sender" #TODO signature of sender = sign(myName, myHash)
saved = False

#so long as bs hasn't confirmed saving, retry
while not saved:
  #Create TCP/IP socket
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  #connecting to the Backup server
  bs_address = ('localhost',2131) #TODO change localhost to correct IP address
  print "Trying to connect to server at %s on port %d" %bs_address
  s.connect(bs_address)

  #Sending data #TODO what separator to use?
  data = myName+"---"+filename+"---"+encrypted+"---"+mySign+"---"+myHash
  s.sendall(data)

  stat = s.recv(buf)
  if not " ".join(stat.split()[:3]) == "Log saved at":
    if stat=="Imposter":
      print "Oh no, got caught"
    elif stat=="Integrity compromised":
      print "Tampering was detected..."
  else: #Means the log was saved
    saved = True  
    print "Backup saved, leaving loop"

print "Sending final ACK"
s.sendall("Final ACK")
print "Closing connection"
s.close()
print "Client finished"
