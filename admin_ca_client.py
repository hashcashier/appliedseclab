import socket
import sys
from os.path import join
from os import getcwd
import ssl

#directory in which to save files
buf = 1024 #size of buffer

#Create TCP/IP socket
s = ssl.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM))

#connecting to the cache
server_address = ('192.168.2.173', 8888) #TODO change address and port number
#print 'Trying to connect to server at %s on port %d' % server_address
s.connect(server_address)

message = "A"
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

[generated, revoked, serial]=data.split(" ")

print generated+"\n"+revoked+"\n"+serial
fd = open(join(client_dir,filename), "wb")
fd.write(data)
fd.close()
#print 'Saved. To bed now'
