#!/usr/bin/python

##########################
# Simple server that listens for connection, starts thread per client.
##########################

import socket
import sys
import threading
import json
import subprocess
import ssl
from os import getcwd
from os.path import join

buf=10000
home_dir ="/home/imovies/appliedseclab/bash/"
#home_dir="/home/diane/Documents/ETH/SecLab/project/code/appliedseclab/bash/"

class ClientThread(threading.Thread):

  def __init__(self, ip, port, socket):
    threading.Thread.__init__(self)
    self.ip = ip
    self.port = port
    self.socket = socket
    print "[+] New thread started for "+ip+":"+str(port)
  
  def parse(self, data):
    """
    The parse function, parses the data and runs the proper script.
    
    It returns the message to send back if all is well. Else -1.
    """
    #separate the flag from the json string
    parts = data.split("_",1)
    flag = parts[0]
    data = parts[1]
    print data
    dict_={}
    strings = []
    #check if valid request
    if flag not in {"G", "R", "RA", "S", "RP"}:
	return
    #load the json string as a dictionary
    if flag in {"G","S", "RA"}: #Flags that can load as json
      try:
        dict_=json.loads(data)
      except ValueError:
        print "Wrong JSON encoding"
        return -1
      except: 
        print "unexpected JSON decoding error"
        return -1
    elif flag=="R": #Sending two raw data files, can't json encode
      strings=data.split(">>>>>>VERY OBVIOUS SEPARATOR<<<<<<",2)
      #print strings
      uname = strings[0]
      cert_str=strings[1]
      pkey_str=strings[2]
      dict_["uname"]=uname
      dict_["cert"]=cert_str
      dict_["pkey"]=pkey_str
    elif flag=="RP": #Sending one raw data file, can't json encode
      strings=data.split(">>>>>>VERY OBVIOUS SEPARATOR<<<<<<",1)
      uname=strings[0]
      p12=strings[1]
      dict_["uname"]=uname
      dict_["p12"]=p12
    """
    Here we check that the necessary arguments are given. 
    G arguments : 	uname
			email
			adminFlag = employee by default 
    R arguments: 	uname
			cert (contents of file to revoke)
			pkey (contents of corresponding pkey file)
    RA arguments: 	uname
    
    S arguments : 	just says {"stats":1}
    """
    if flag=="S":
      #call bash stat script
      exitcode=subprocess.call(home_dir+"stats.sh", shell=True)
      print exitcode
      if not exitcode: #all went well
	#open corresponding .p12 file
	fd = open(join(home_dir, "demoCA/stats"), "r")
	resp = fd.read()
	fd.close()
	return resp
      return -1
    elif flag=="G":
      if not dict_.has_key("uname") or not dict_.has_key("email"):
        #returning -1 as error
	return -1
      else:
	#call bash generate script with arguments uname email employee
	exitcode=subprocess.call(home_dir+"create-key-and-csr.sh "+dict_["uname"]+" "+dict_["email"]+" employee", shell=True)
 	print exitcode
        if not exitcode: #exited without a problem"
	  #open corresponding .p12 file
	  fd = open(join(home_dir, "certs/users/"+dict_["uname"]+"/"+dict_["uname"]+".p12"), "rb")
	  resp = fd.read()
	  fd.close()
	  return resp
	else:
	  return -1
    elif flag=="R":
      if not dict_.has_key("uname") or not dict_.has_key("cert") or not dict_.has_key("pkey"):
	#returning -1 as error
	return -1
      else: #This means we want to delete specific key
        # save cert and pkey temporarily to files
        cert_str = dict_["cert"]
	pkey_str = dict_["pkey"]
	fd=open(join(home_dir,uname+".rev-cert"), "wb")
	fd.write(cert_str)
	fd.close()
	kd=open(join(home_dir,uname+".rev-key"), "wb")
	kd.write(pkey_str)
	kd.close()
	#verify they match
	match=subprocess.call(home_dir+"verify-cert-key.sh "+uname+" "+home_dir+uname+".rev-cert "+home_dir+uname+".rev-key", shell=True)
	print match
        if match:
          return -1
	#call bash revoke script
	exitcode=subprocess.call(home_dir+"revoke-one.sh "+home_dir+uname+".rev-cert", shell=True)
	print exitcode
	if not exitcode: #finished with no problem
	  #open crl file
	  fd = open(join(home_dir, "certs/crl/my-root-crl.pem"), "rb")
	  resp = fd.read()
	  fd.close()
	  return resp
	else:#error
	  return -1
    elif flag=="RP":
      if not dict_.has_key("uname") or not dict_.has_key("p12"):
	#returning -1 as error
	print "NOTHING"
	return -1
      else: #This means delete cert is p12 file
        p12_str = dict_["p12"]
	fd=open(join(home_dir,uname+".rev-p12"),"wb")
	fd.write(p12)
	fd.close()
	#get certificate from p12
        getcert=subprocess.call(home_dir+"cert-from-pkcs12.sh "+home_dir+uname+".rev-p12 "+home_dir+uname+".rev-cert", shell=True)
	print "GOT CERTIFICATE"
	#call bash revoke script
	exitcode=subprocess.call(home_dir+"revoke-one.sh "+home_dir+uname+".rev-cert",shell=True)
	if not exitcode: #finished wth no problem
	  #open crl file
	  fd = open(join(home_dir, "certs/crl/my-root-crl.pem"),"rb")
	  resp=fd.read()
	  fd.close()
	  return resp
	else: #error
	  return -1
    elif flag=="RA":
      if not dict_.has_key("uname"):
        #returning -1 as error
	return -1
      else: #We can revoke all certificates for user "uname"
        #call bash script revoke-all.sh uname
	exitcode=subprocess.call(home_dir+"revoke-all.sh "+dict_["uname"], shell=True)
	print exitcode
	if not exitcode: #finished with no problem
	  #open crl file
	  fd = open(join(home_dir, "certs/crl/my-root-crl.pem"), "rb")
	  resp = fd.read()
	  fd.close()
	  return resp
	return -1
    else: #Some unforseen error	  
      return -1

  def run(self):    
    print "Connection from : "+ip+":"+str(port)
      
    # receive and parse data
    data = self.socket.recv(buf)
    #print "Received: "+data
    resp = self.parse(data)
    if resp==-1:
      resp = "error"
      print resp
    #send response
    self.socket.sendall(str(resp))
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

sock = ssl.wrap_socket(s, certfile="/home/imovies/appliedseclab/bash/certs/ca/my-root-ca.crt.pem", keyfile="/home/imovies/appliedseclab/bash/certs/ca/my-root-ca.key.pem", server_side=True, do_handshake_on_connect=False)

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
while True: 
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
