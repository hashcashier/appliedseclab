############################
# The Generate, and revocate objects used by the CA
############################

import sys
from OpenSSL import crypto, SSL
from certgen import *
from certrev import *
from os.path import exists

class Generator:
  '''
        This class is a generator used to process the request. 
        The type of request processes is certificate generation
        Arguments:
          uname : a string with the username
          name : a dictionary containing all option (see cert gen for option types)
          serial_num : the certificate serial number
  '''
 
  def __init__(self, uname, name, issuer, serial_num):
    self.uname = uname
    self.name = name
    self.issuer = issuer
    self.serial_num = serial_num
   
    # response strings, must be the HTTP response that will eventually be sent
    self.error_resp = "There was an error in generation"
    self.resp = "Something has been generated"

    ## about the issuer
    #issuer_key = ""
    #issuer_cert = ""
    #issuer = (issuer_key, issuer_cert)
    self.timestamps = (0,3600)

  def process(self):
    #TODO : errors and logs
    #generate public/private key pair
    pkey = createKeyPair(TYPE_RSA, 2048)
    #Genrate certificate request
    req = createCertRequest(pkey, "sha1", **self.name)
    #creater signed certificate from request
    cert = createCertificate(req, self.issuer, self.serial_num, (0,365000), "sha1")
    # write certificate to a file
    # create PKCS#12 archive containing: pkey, cert... TODO issuerCert?
    file_name = self.uname+".p12"
    file = open(file_name, "wb")
    p12 = crypto.PKCS12()
    p12.set_certificate(cert)
    p12.set_privatekey(pkey)
    #?#p12.set_ca_certificates(issuer_Cert)
    file.write(p12.export())
    file.close()
    # TODO add file contents to resp
    return self.resp

class Revocator:
  """
  This class is a revocator, it receives the certificate to revoke (by name) and when processed   returns the crl in form or response
  Arguments: 	uname
		crl
		issuer
		reason, unspecified by default
  """
  def __init__(self, uname, crl, issuer, reason="unspecified"):
    self.uname = uname
    self.crl = crl
    self.issuer = issuer
    self.reason = reason
    self.error_resp = "There was an error in revocation"
    self.resp = "The certificate was revocated"

  def load_cert(self):
    """
    Returns the certificate in X509 form if it exists, None if it doesn't. 
    """
    filename = self.uname+".p12"
    if exists(filename):
      cert = crypto.load_pkcs12(open(filename).read()).get_certificate()
      return cert
    else:
      return

  def process(self):
    #load the certificate to revoke
    cert=self.load_cert()
    if cert==None:
      return self.error_resp
    #create revocation for this certificate, then update the crl
    rev = createRev(cert.get_serial_number(), self.reason)
    new_crl = update_CRL(rev, self.crl)
    #sign the new crl
    (i_cert,i_key)=self.issuer
    #write new crl to a file
    filename = self.reason+"crl.pem" # doing this for tests
    file=open(filename, "wb")
    file.write(new_crl.export(i_cert, i_key, crypto.FILETYPE_PEM))
    file.close()
    #TODO errors?
    return self.resp 
