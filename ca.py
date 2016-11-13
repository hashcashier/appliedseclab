'''
    Simple socket server using threads
'''
 
import socket
import sys

def error():
    '''
	Good old error function. Returns an error response to send to the client
    '''
    print 'Error: received an invalid request'
    return 'Not a valid request. Usage: FLAG Username [Options]';

def generate(uname, options): # options will be : name, email, company = 'iMovies', address= '' ):
    '''
	This function generates a certificate with the given information. And returns what to send back 
    '''
    print 'Generated a certificate for ', uname
    response = 'Hello ' + uname + ", we have generated a certificate for you with options: " + options + '!'
    return response;

def revoke (uname, reason=''):
    '''
	This function revokes a certificate with the given information, and returns what to send back
    '''
    print 'Revoked certificate of user %s' %uname
    response = 'Hello ' + uname +', we have revoked your certificate, with for reason: ' + reason
    return response;

#defining some useful functions TODO: put these in classes or modules or threads or something
def parse (data):
    '''
	For now, this function parses data (a string) and returns a string that is the response
	This will later be the function that returns whether we should run Generate or Revoke and with what information, or return a parse error 
    '''
    
    flag = ''
    request = {'uname':'', 'options':''}
    accepted_flags = {'G', 'R'}
    #parse data to pick a function
    #Data of the form: FLAG Username Options 
    #FLAG is G for generate and R for revoke; Options can be however many (and anything for now)
    parts = data.split(' ', 2)
    if len(parts) >=3:
        flag = parts[0]
        request['uname'] = parts[1]
        request['options'] = parts[2]
    print "Received: %s" %data, "... parsing"
    #check that the required data (FLAG and Username") has been provided 
    if ( flag not in accepted_flags) | (request['uname']==''):
            def process(request):
		return error();
    else :
        if flag=='G':
	    def process(request):
		return generate(request['uname'], request['options']);
        else :
	    def process(request):
		return revoke(request['uname'], request['options']);
    return process, request;

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
while k<1: #how many connections do we want to accept? while 1 for infinite loop
    #wait to accept a connection - blocking call
    conn, client_address = s.accept()
    print 'Connected with ' + client_address[0] + ':' + str(client_address[1])
    
    #receive and return data, blocking call to recv
    buf = 1024
    data = conn.recv(buf)
    #parse data to pick a function
    #Data of the form: FLAG Username Options 
    #FLAG is G for generate and R for revoke; Options can be however many (and anything for now)
    process, request = parse(data)
    response = process(request);
    print 'Parsed. Reponding: ', response
    conn.sendall(response)     
    print "Closing connection with client ", client_address
    conn.close
    k+=1
print "closing socket on server at %s port %d" %server_address
s.close()
print "That's all folks"
