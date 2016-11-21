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
Arguments: 	flag G or R
		uid = "uname"
		FirstName +
		LastName = "CN"
		email = "emailAddress"
		adminFlag = "OU" 
"""
if len(sys.argv) < 7:
  print "Usage: python client.py <flag> <uid> <FirstName> <LastName> <email> <adminFlag>"
  sys.exit()

[flag, uname, firstname, lastname, email, adminFlag] = sys.argv[1:]
message = flag+'_'+'{"uname":"'+uname+'","CN":"'+firstname+' '+lastname+'","emailAddress":"'+email+'","O":"iMovies","OU":"'+adminFlag+'"}'

#file to save response at
filename = "crl.pem" if flag=="R" else uname+".p12"

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
