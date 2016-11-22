#
# Copyright (C) Diane Adjavon
# See LICENSE for details

'''
Certificate revocation module
'''

from OpenSSL import crypto
#from time import gmtime

TYPE_RSA = crypto.TYPE_RSA
TYPE_DSA = crypto.TYPE_DSA


def createRev(serial, reason="unspecified"):
  """
  Create a certificate revocation request.
  Arguments: serial the serial number of the certificate to revoke
	     reason can be : 	'unspecified'
				'keyCompromise'
				 'CACompromise'
				 'affiliationChanged'
				 'superseded'
				 'cessationOfOperation'
				 'certificateHold'


  Returns: a revoked object
  """
  r = crypto.Revoked()
  r.set_serial(hex(serial))
  if reason in r.all_reasons():
    r.set_reason(reason)
  #r.set_rev_date(gmtime(0))
  return r

def update_CRL(revoked, crl):
  """
  Includes revoked object into crl
  Arguments : 	the revoked object to be added 
		the crl to add it to
  Returns: a crl object
  """
  #print crypto.dump_certificate(crypto.FILETYPE_PEM, revoked)
  #print str(revoked)
  print crypto.dump_crl(crypto.FILETYPE_PEM, crl)
  crl.add_revoked(revoked)
  print "Added revoked :"+str(revoked)
  #crl.set_lastUpdate(when) ##need to figure out ASN.1 Generalized time
  return crl
