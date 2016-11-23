#!/bin/bash

#Before running this, verify that the cert file matches the given key file 

#Arguments:	FILENAME = full path to a valid pem certificate to revoke
#Revokes the given file, then updates the crl

#The crl, saved under certs/crl/my-root-crl.pem is to be scp to the WS

FILENAME=$1

#revoke given certificate
openssl ca \
  -revoke ${FILENAME} \
  -keyfile certs/ca/my-root-ca.key.pem \
  -cert certs/ca/my-root-ca.crt.pem \

# create initial empty crl
openssl ca \
  -gencrl \
  -keyfile certs/ca/my-root-ca.key.pem \
  -cert certs/ca/my-root-ca.crt.pem \
  -out certs/crl/my-root-crl.pem 

#one has been revoked, modify revoked file
gawk -i inplace '{$1=$1+1}1' demoCA/revoked


#delete files
rm ${FILENAME}

