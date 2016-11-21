import socket
import sys
import threading
import time
from datetime import date
from os.path import join
from os import getcwd

log_dir =join(getcwd(),"logs/") #TODO set this to correct place for logs

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
    data = self.socket.recv(buf) #TODO read more data?
    #data = ""
    #while True:
    #  data_in = self.socket.recv(buf)
    #  if not data_in: break
    #  data+=data_in
    #print data 
    #Parse data to retrieve Sender, Encrypted File E, Sign(Sender)
    (sender, filename, E) = data.split("---") #for tests TODO parse
    
    #####
    #  If we get here, we assume authentication and integrity are ok
    #####

    #open file named filename_sender_timestamp
    timestamp = time.time()
    filename = filename+"_"+sender+"_"+str(timestamp)
    fd = open(join(log_dir,filename), "w")
    #save E to file
    fd.write(E)
    #set file permissions TODO 
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
print "[-] Closing socket on server at %s port %d" %server_address
s.close()
print "[-] Hasta la bye, bye"
