from OpenSSL import crypto, SSL
from pprint import pprint
from time import gmtime, mktime
from os.path import exists, join

CERT_FILE = "ca.crt"
KEY_FILE = "ca.key"
CRL_FILE = "crl.pem"

def create_ca_cert(cert_dir):
  """
  If ca.crt and ca.key don't exist in cert_dir, create a new
  self-signed cert and keypair and write them into that directory.
  """

  if not exists(join(cert_dir, CERT_FILE)) or not exists(join(cert_dir, KEY_FILE)):
            
    # create a key pair
    k = crypto.PKey()
    k.generate_key(crypto.TYPE_RSA, 2048)
    # create a self-signed cert
    
    cert = crypto.X509()
    cert.get_subject().C = "SW"
    cert.get_subject().L = "Zuerich"
    cert.get_subject().O = "iMovies"
    cert.get_subject().CN = "CA"
    cert.set_serial_number(1000)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(10*365*24*60*60)
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(k)
    cert.sign(k, 'sha1')
     

    open(join(cert_dir, CERT_FILE), "wt").write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
    open(join(cert_dir, KEY_FILE), "wt").write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k))
    
def create_crl(cert_dir, (issuer_cert, issuer_key)):
  """
  If crl.pem does not exist in cert_dir, create a new one signed by issuer_key with issuer_cert  and write it into that directory
  """
  if not exists(join(cert_dir, CRL_FILE)):
    #create a crl
    crl = crypto.CRL()
    buf = crl.export(issuer_cert, issuer_key, crypto.FILETYPE_PEM)
    open(join(cert_dir, CRL_FILE), "wb").write(buf)

def get_ca_key(cert_dir):
  if exists(join(cert_dir, KEY_FILE)):
    # open file and read into buffer
    buf = open(join(cert_dir, KEY_FILE)).read()
    # load a key from buffer
    ca_key = crypto.load_privatekey(crypto.FILETYPE_PEM, buf)
    return ca_key
  else:
    return 

def get_ca_cert(cert_dir):
  if exists(join(cert_dir, CERT_FILE)):
    #open file and read into buffer
    buf = open(join(cert_dir, CERT_FILE)).read()
    #Load certificate from buffer
    ca_cert = crypto.load_certificate(crypto.FILETYPE_PEM, buf)
    return ca_cert
  else:
    #recursive thing, create self signed, get it, then return what you get?
    return

def get_crl(cert_dir):
  if exists(join(cert_dir, CRL_FILE)):
    #open file and read into buffer
    buf = open(join(cert_dir, CRL_FILE)).read()
    # load crl from buffer
    crl = crypto.load_crl(crypto.FILETYPE_PEM, buf)
    return crl
  else:
    return
#########################
#	do the thing	#
#########################

#create_self_signed_cert("./")
