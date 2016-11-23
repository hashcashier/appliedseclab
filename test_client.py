#!/usr/bin/python
import socket
import sys
from os.path import join
from os import getcwd
import ssl

#directory in which to save files
client_dir = join(getcwd(),"client")
buf = 1024 #size of buffer


#check number of arguments
"""
Arguments: 	flag G 
			uid = "uname"
			FirstName +
			LastName = "CN"
			email = "email"
			adminFlag = "OU"
 	OR	flag R
			jsonencoded{cert, pkey} 
	 	flag RA
			uname
	OR
		flag S
			none
"""

if len(sys.argv) < 2:
  print "Not enough arguments" 
  sys.exit()
else:
  flag = sys.argv(1)

if flag =="S"
  message = flag
elif flag == "G":
  [uname, email, adminFlag] = sys.argv[2:]
  message = flag+'_'+'{"uname":"'+uname+'","CN":"'+uname+'","email":"'+email+'","O":"iMovies","OU":"'+adminFlag+'"}'
elif flag=="R":
  dict_=sys.argv[2]
  message = flag+'_'+dict_
elif flag=="RA":
  uname=sys.argv[2]
  message = flag+'_'+'{"uname":'+uname+'"}'

#file to save response at
filename = "crl.pem" if (flag=="R" or flag=="RA") else "download.p12"

#Create TCP/IP socket
s = ssl.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM))

#connecting to the cache
server_address = ('localhost', 8888) #TODO change address and port number
print 'Trying to connect to server at %s on port %d' % server_address
s.connect(server_address)

#making request
s.sendall(message)

# receive response 
data = ""
while True: 
  data_in= s.recv(buf)
  if not data_in: break
  data+=data_in

#check if data is error
if data=="error":
  print "Error, closing"
  sys.exit()

print "\n Saving to file ./client/"+filename 
fd = open(join(client_dir,filename), "wb")

fd.write(data)
fd.close()
print 'Saved. To bed now'
