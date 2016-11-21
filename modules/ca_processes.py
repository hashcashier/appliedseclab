############################
# The Generate, and revocate objects used by the CA
############################

import sys
from OpenSSL import crypto, SSL
from certgen import *
from certrev import *
from os.path import exists, join
from os import getcwd, chmod, listdir

#the following line is necessary to check existence of files in Revocator.process(), otherwie it looks for certificates within code/modules
cert_dir = "./certs" #TODO change to final directory

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
    self.error_resp = "error generation"
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
    file_name = str(self.serial_num)+self.uname+".p12"
    file = open(join(cert_dir,file_name), "wb")
    p12 = crypto.PKCS12()
    p12.set_certificate(cert)
    p12.set_privatekey(pkey)
    #?#p12.set_ca_certificates(issuer_Cert)
    file.write(p12.export())
    file.close()
    chmod(join(cert_dir, file_name), 0600)
    # TODO add file contents to resp
    self.state=1
    self.resp = file_name
    return self.resp

  def generate_response(self):
    """
    Look at the state of self: 0 means unprocessed, 1 means processed correctly, with filename/response content in self.resp, -1 means not processed correctly with error in self.error_resp
    Returns: HTTP to send file if correct, HTTP error message in plain text if error, nothing if unprocessed
    """
    hdr = ""
    content = ""
    if self.state == 1 : 
      hdr = "HTTP /1.1 200 OK\nContent-Type: application/x-pki12\nConnection: Closed\n\n"
      in_file = open(join(cert_dir,self.resp),"rb")
      content = in_file.read()
    if self.state == -1 : 
      hdr = "HTTP /1.1 400 Bad Request\nContent-Type: text/plain\nConnection: Closed\n\n"
      content = self.error_resp
    return content #hdr+content

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
    self.error_resp = "error revocation"
    self.resp = "The certificate was revoked"
    self.state = 0
  
  def load_certs(self):
    """
    Returns the certificate in X509 form if it exists, None if it doesn't. 
    """
    certs=[]
    filename = self.uname+".p12"
    #print "filename is: "+filename
    #print "path to file is :"+join(cert_dir,filename)
    #if exists(join(cert_dir,filename)):
      #print "File exists"
    for f in listdir("./certs"):
      if f.endswith(filename):
        print f
        certs.append(crypto.load_pkcs12(open(join(cert_dir,f)).read()).get_certificate())
    if certs==[]:
      return
    else:
      print certs
      return certs

  def load_cert(self):
    """
    Returns the certificate in X509 form if it exists, None if it doesn't. 
    """
    filename = self.uname+".p12"
    #print "filename is: "+filename
    #print "path to file is :"+join(cert_dir,filename)
    #if exists(join(cert_dir,filename)):
      #print "File exists"
    for f in listdir("./certs"):
      if f.endswith(filename):
        print f
        cert = crypto.load_pkcs12(open(join(cert_dir,f)).read()).get_certificate()
    if cert==None:
      return
    else:
      return cert
  
  def process(self):
    #load the certificate to revoke
    certs=self.load_certs()
    #TODO CHANGES HERE
    new_crl = self.crl
    for cert in certs:
      if cert==None:
        self.state = -1
        return self.error_resp
      #create revocation for this certificate, then update the crl
      rev = createRev(cert.get_serial_number(), self.reason)
      new_crl = update_CRL(rev, new_crl)
    #TODO CHANGES UNTIL HERE
    #sign the new crl
    (i_cert,i_key)=self.issuer
    #write new crl to a file
    filename = "crl.pem"
    file=open(filename, "wb")
    file.write(new_crl.export(i_cert, i_key, crypto.FILETYPE_PEM))
    file.close()
    chmod(join(cert_dir, filename), 0600)
    #TODO errors?
    self.state = 1
    self.resp = filename
    return self.resp 

  def generate_response(self):
    """
    Look at the state of self: 0 means unprocessed, 1 means processed correctly, with filename/response content in self.resp, -1 means not processed correctly with error in self.error_resp
    Returns: HTTP to send file if correct, HTTP error message in plain text if error, nothing if unprocessed
    """
    hdr = ""
    content = ""
    if self.state == 1 : 
      hdr = "HTTP /1.1 200 OK\nContent-Type: application/pkix-crl\nConnection: Closed\n\n"
      in_file = open(join(cert_dir,self.resp),"rb")
      content = in_file.read()
    if self.state == -1 : 
      hdr = "HTTP /1.1 400 Bad Request\nContent-Type: text/plain\nConnection: Closed\n\n"
      content = self.error_resp
    return content#hdr+content
