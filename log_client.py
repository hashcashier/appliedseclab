import socket
import sys
from os.path import exists
import aes #TODO put into modules

"""
Integrity and Authentication checked by SSL socket 

Arguments:	sender name
		filename
		password filename

"""

#check number of arguments
if len(sys.argv) < 4:
  print "Usage : python log_client <sender> </path/to/filename> </path/to/password>"
  sys.exit()

buf = 4096
myName = sys.argv[1] #TODO CA or WS depending on the case
filename = sys.argv[2]
passfile = sys.argv[3]

#check if file exists
if not exists(filename):
  print "File not found"
  sys.exit()

#check if password file exists
if not exists(passfile):
  print "Passfile not found"
  sys.exit()

#read from file
fd = open(filename, "rb")
myFile = fd.read()
fd.close()

#read from password file
pd = open(passfile, "rb")
key = pd.read()
pd.close()

#encrypt, hash
cipher = aes.AESCipher(key)
encrypted = cipher.encrypt(myFile)
saved = False

#so long as bs hasn't confirmed saving, retry
while not saved:
  #Create TCP/IP socket
  #TODO SSL wrapper
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  #connecting to the Backup server
  bs_address = ('localhost',2131) #TODO change localhost to correct IP address
  print "Trying to connect to server at %s on port %d" %bs_address
  s.connect(bs_address)

  #Sending data #TODO what separator to use?
  data = myName +'---'+filename+'---'+ encrypted#myName+"---"+filename+"---"+encrypted+"---"+mySign+"---"+myHash
  s.sendall(data)

  stat = s.recv(buf)
  print stat
  saved = True
  break
  #  saved = True  
  # print "Backup saved, leaving loop"

print "Sending final ACK"
s.sendall("Final ACK")
print "Closing connection"
s.close()
print "Client finished"
