'''
    Simple socket server using threads
'''
 
import socket
import sys

 
HOST = 'localhost'   # Symbolic name, meaning all available interfaces
PORT = 8888 # Arbitrary non-privileged port
server_address = (HOST, PORT)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created on host %s port %d' %server_address
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #so no address already in use

#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket bind complete'
 
#Start listening on socket
s.listen(10)
print 'Socket now listening'
k=0
#now keep talking with the client
while k<1:
    #wait to accept a connection - blocking call
    conn, client_address = s.accept()
    print 'Connected with ' + client_address[0] + ':' + str(client_address[1])
    
    #receive and return data, blocking call to recv
    buf = 1024
    data = conn.recv(buf)
    print "Received: %s" %data
    conn.send("We have received your data. Thank you. ")     
    print "Closing connection with client ", client_address
    conn.close
    k+=1
print "closing socket on server at %s port %d" %server_address
s.close()
print "That's all folks"
