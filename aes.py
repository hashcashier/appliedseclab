import base64
import hashlib
from Crypto.Cipher import AES
from Crypto import Random
import sys
from os.path import exists

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS) 
unpad = lambda s : s[:-ord(s[len(s)-1:])]

class AESCipher:
    def __init__( self, key ):
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt( self, plaintext ):
        plaintext = pad(plaintext)
        iv = Random.new().read( AES.block_size )
        cipher = AES.new( self.key, AES.MODE_CBC, iv )
        return base64.b64encode( iv + cipher.encrypt( plaintext ) ) 

    def decrypt( self, ciphertext ):
        ciphertext = base64.b64decode(ciphertext)
        iv = ciphertext[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv )
        return unpad(cipher.decrypt( ciphertext[16:] ))

if len(sys.argv)<3:
  print "Usage: python aes.py -p <plaintext_file> <key>"
  sys.exit()

plaintext_file = sys.argv[1]
if not exists(plaintext_file):
  print "File not found"
  sys.exit()

fd = open(plaintext_file, "r")
plaintext = fd.read()
fd.close()

key = sys.argv[2]
cipher = AESCipher(key)
ct = cipher.encrypt(plaintext)
print "Ciphertext: "+ct
pt = cipher.decrypt(ct)
print "Decrypted: "+pt

