#!/usr/bin/python

##########################
# Simple server that listens for connection, starts thread per client.
##########################

import socket
import sys
import threading
import json
from OpenSSL import crypto, SSL
from modules import gen_ca, ca_processes
import ssl
from os import getcwd
from os.path import join

buf=1024
######################
# get CA information #
######################
cert_dir = "/home/imovies/appliedseclab/certs/"
gen_ca.create_ca_cert(cert_dir)
issuer = (gen_ca.get_ca_cert(cert_dir),gen_ca.get_ca_key(cert_dir))
serial = 1 #TODO randomize serial number
gen_ca.create_crl(cert_dir, issuer)
current_crl=gen_ca.get_crl(cert_dir)

class ClientThread(threading.Thread):

  def __init__(self, ip, port, socket):
    threading.Thread.__init__(self)
    self.ip = ip
    self.port = port
    self.socket = socket
    print "[+] New thread started for "+ip+":"+str(port)
  
  def parse(self, data):
    """
    The parse function, parses the data to get the proper type of object
    Arguments:	data is the input data from client
		We assume for now that data is a flag G or R concatenated with character _ concatenated with a json encoding of an array of key,value pairs
		
    		self refers to the current thread	
    Returns: 	a Generator or Revocator correctly initialized, or None if parse Error
    """
    global serial
    #TODO Parse and remove the HTTP header
    #separate the flag from the json string
    parts = data.split("_",1)
    flag = parts[0]
    data = parts[1]
    #print "flag is :"+flag
    #print "json_data is : "+data
    #print "data type is : " +str(type(data))
    
    #check valid request
    if flag not in {"G", "R"}:
	return
    #load the json string as a dictionary
    try:
      dict_=json.loads(data)
    except ValueError:
      print "Wrong JSON encoding"
      return
    except: 
      print "unexpected JSON decoding error"
      return 
    """
    Here we check that the necessary arguments are given. 
    G arguments : 	uname
			name = CN
    R arguments: 	uname
    """
    if flag=="G":
      if not dict_.has_key("uname") or not dict_.has_key("CN"):
        #returning None as error
	return None
      else:
	#reformat the arguments
	uname = dict_["uname"]
	del dict_["uname"]
	#create the Generator object
	Gen = ca_processes.Generator(uname, dict_, issuer, serial)
	#update the serial number
	serial +=1
	#return object
	return Gen
    elif flag=="R":
      if not dict_.has_key("uname"):
	#returning None as error
	return None
      else:
	#reformat the arguments
	uname = dict_["uname"]
	reason = "unspecified" if not dict_.has_key("reason") else dict_["reason"]
	#create the Revocator object
	Rev = ca_processes.Revocator(uname, current_crl, issuer)
	#return object
	return Rev	  
  
  def run(self):    
    print "Connection from : "+ip+":"+str(port)
      
    #TODO
    # receive and parse data
    data = self.socket.recv(buf)
    print "Received: "+data
    Object = self.parse(data)
    if Object==None:
      #resp = "HTTP /1.1  400 Bad Request\nContent-type: text/plain\n Connection: Closed\n\nParsing error"
      resp = "error"
      print resp
    else:
      f_name = Object.process()
      print "file processed: "+f_name
      resp = Object.generate_response()
      print "Data processed. "#+resp
      if resp.split()[0]=="error":
	resp = "error"
    # THIS IS A TEST OF GENERATOR
    #name = {'C': 'SW', 'O': 'iMovie', 'CN':'test'}
    #Gen = ca_processes.Generator(data, name, issuer, serial)
    #resp = Gen.process()
    #print "Generator says : " +resp
    
    
    #THIS IS A TEST OF REVOCATOR
    #Rev = ca_processes.Revocator("test", current_crl, issuer)
    #resp2 = Rev.process()
    #print "Revocator says :"+resp2

    #send response
    self.socket.sendall(resp)
    ## end connection
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

HOST = '0.0.0.0' #Symbolic name meaning all available interfaces
PORT = 8888 #Arbitrary non privileged port
server_address = (HOST, PORT)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print "[+]Socket created on host %s port %d" %server_address
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #so no 'address already in use' after crash

sock = ssl.wrap_socket(s, certfile="/home/imovies/appliedseclab/certs/ca.crt", keyfile="/home/imovies/appliedseclab/certs/ca.key", server_side=True, do_handshake_on_connect=False)

#Bind socket to local host and port
try:
  sock.bind((HOST, PORT))
except socket.error as msg:
  print "[!!]Bind failed. Error Code: "+str(msg[0])+ " Message "+msg[1]
  sys.exit()

print "[+]Socket bind complete"

#Start listening on socket
sock.listen(10)
print "[+]Socket now listening"
k=0
threads = [] #to be able to wait for all connections to end

#Connection from client and open a thread
while k<1: #TODO set to while true after debugging
  #wait to accept a connection - blocking call
  (clientSocket, (ip, port)) = sock.accept()
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
