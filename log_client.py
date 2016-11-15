import socket
import sys

buf = 1024
myName = "Sender" #TODO CA or WS depending on the case
mySign = "Sender" #TODO signature of sender

#Create TCP/IP socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#connecting to the Backup server
bs_address = ('localhost',2131) #TODO change localhost to correct IP address
print "Trying to connect to server at %s on port %d" %bs_address
s.connect(bs_address)

#Sending data
message = raw_input("Your message: ")
data = myName+"\n"+message+"\n"+mySign
s.sendall(data)

# Wait for response
resp = s.recv(buf)
while resp=="resend":
  #resend
  s.sendall(data)
  #check status
  resp = s.recv(buf)

if resp=="Imposter": #sender doesn't match signature
  print "Oh no, got caught" 
elif resp =="Unable to backup": #too many resends
  print "Backup problem, keep logs locally"
else: #Log saved at + timestamp received
  print "Backup done, can delete logs"

print "Sending final ACK"
s.sendall("Final ACK")
print "Closing connection"
s.close()
print "Client finished"
