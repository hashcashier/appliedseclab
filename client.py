import socket
import sys

buf = 1024 #size of buffer

#Create TCP/IP socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#connecting to the cache
cache_address = ('localhost', 8888)
print 'Trying to connect to server at %s on port %d' % cache_address
s.connect(cache_address)

#Chatting!
message = raw_input('Your message: ')
s.sendall(message)
# receive new size of buffer
#buf = int(s.recv(buf))
#s.send('OK')
# receive message 
data = ""
while True: 
  data_in= s.recv(buf)
  if not data_in: break
  data+=data_in

print 'Received : ' , data  
print 'To bed now'
