import socket
import sys
import threading
import time
from datetime import date

buf= 1024

class ClientThread(threading.Thread):

  def __init__(self, ip, port, socket):
    threading.Thread.__init__(self)
    self.ip = ip
    self.port = port
    self.socket = socket
    print "[+] New thread started for "+ip+":"+str(port)

  def run(self):
    counter =  0
    #Receive data
    data = ""
    while True:
      data_in = self.socket.recv(buf)
      if not data_in: break
      data+=data_in 
    #Parse data to retrieve Sender, Encrypted File E, Sign(Sender)
    (Sender, E, Sign) = ("sender", data, "sender") #for tests TODO parse
    #verify Signature (is really sender) else raise an error
    if Sender!=Sign: #TODO retrieve Sender from signature
      print "Sender is not who they say they are"
      #send bad authentication to "sender"
      self.socket.sendall("Imposter")
      #cleanly close the connection
      print "[-] Closing connection with "+ip+":"+port
      self.socket.close()
      return
    #hash(E)
    hash_data = E #TODO actually hash it
    #conn.send(E)
    self.socket.sendall(E)
    #Wait for sender to verify
    OK = int(self.socket.recv(buf)) #can be 1 for OK, 0 for not OK
    if not OK:
      if counter <3:
        #ask for resend
        print "Requesting resend" 
        self.socket.sendall("resend")
        #increase send counter by one
	counter+=1
      else: 
        #send and raise an error
        print "Too many resends, suspect tampering"
	self.socket.sendall("Unable to backup")
        #cleanly close connection
        print "[-] Closing connection with "+ip+":"+port
	self.socket.close()
        return
    else: #All seems well, proceed
      #open file named Sender_timestamp
      timestamp = str(time.time())
      filename = Sender+"_"+timestamp
      fd = open(filename, "w")
      #save E to file
      fd.write(E)
      #set file permission TODO ???
      #send all ok
      self.socket.sendall("Log saved at "+str(date.fromtimestamp(timestamp)))
      
    #wait for final ack
    print "Waiting for confirmation"
    ack = self.socket.recv(buf)
    print "Received final message" #TODO check if good or bad
    print "[-] Closing connection"
    self.socket.close()
    
#########################################
#					#
#		Main Thread		#
#					#
#########################################

HOST = 'localhost'
PORT = 2131
server_address = (HOST, PORT)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print "[+] Socket created on host %s port %d" %server_address
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1) #avoid "alread in use" if crash

#Bind 
try:
  s.bind(server_address)
except socket.error as msg: 
  print "[!!] Bind failed. Error Code: "+str(msg[0])+" Message "+msg[1]
  sys.exit()

print "[+]Socket bind complete"

#Start listening on socket
s.listen(10)
print "[+]Socket now listening"
k=0
threads = [] # to be able to wait for all connections to end

#Connections from client open a ClientThread
while k<1: #TODO set to while True after debugging
  #wait to accept a connection - blocking call
  (clientSocket, (ip, port)) = s.accept()
  #start a thread
  newThread = ClientThread(ip, port, clientSocket)
  newThread.start()
  threads.append(newThread)
  k+=1

for t in threads:
  t.join()

#Finish it all
print "[-] Closing socket on server at % port %d" %server_address
s.close()
print "[-] Hasta la bye, bye"
