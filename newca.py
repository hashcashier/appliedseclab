##########################
# Simple server that listens for connection, starts thread per client.
##########################

import socket
import sys
import threading
from OpenSSL import crypto, SSL
from gen_ca import *
from ca_processes import Generator, Revocator

buf=1024
######################
# get CA information #
######################
create_ca_cert("./")
issuer = (get_ca_cert("./"),get_ca_key("./"))
serial = 1
create_crl("./", issuer)
current_crl=get_crl("./")

class ClientThread(threading.Thread):

  def __init__(self, ip, port, socket):
    threading.Thread.__init__(self)
    self.ip = ip
    self.port = port
    self.socket = socket
    print "[+] New thread started for "+ip+":"+str(port)

  def run(self):    
    print "Connection from : "+ip+":"+str(port)
      
    #TODO
    # receive and parse data
    # THIS IS A TEST OF GENERATOR
    name = {'C': 'SW', 'O': 'iMovie', 'CN':'test'}
    Gen = Generator("test", name, issuer, serial)
    resp = Gen.process()
    print "Generator says : " +resp
    
    #THIS IS A TEST OF REVOCATOR
    Rev = Revocator("test", current_crl, issuer)
    resp2 = Rev.process()
    print "Revocator says :"+resp2

    ## simple echo service
    data = self.socket.recv(buf)
    print "Received: "+data
    self.socket.send("You sent me : "+data)
    print "Disconnecting from client"
    self.socket.close()
    print "[-] Thread closed on "+ip+":"+str(port)


#########################################
#					#
#					#
#	Beginning of main thread	#
#					#
#					#
#########################################

HOST = 'localhost' #Symbolic name meaning all available interfaces
PORT = 8888 #Arbitrary non privileged port
server_address = (HOST, PORT)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print "[+]Socket created on host %s port %d" %server_address
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #so no 'address already in use' after crash

#Bind socket to local host and port
try:
  s.bind((HOST, PORT))
except socket.error as msg:
  print "[!!]Bind failed. Error Code: "+str(msg[0])+ " Message "+msg[1]
  sys.exit()

print "[+]Socket bind complete"

#Start listening on socket
s.listen(10)
print "[+]Socket now listening"
k=0
threads = [] #to be able to wait for all connections to end

#Connection from client and open a thread
while k<4: #TODO set to while true after debugging
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
print "[-]Closing socket on server at %s port %d" %server_address
s.close()
print "[-]That's all folks!"
