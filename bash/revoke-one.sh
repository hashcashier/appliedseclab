#!/bin/bash

#Before running this, verify that the cert file matches the given key file 

#Arguments:	FILENAME = full path to a valid pem certificate to revoke
#Revokes the given file, then updates the crl

#The crl, saved under certs/crl/my-root-crl.pem is to be scp to the WS

HOMEDIR="/home/imovies/appliedseclab/bash/"
FILENAME=$1

#revoke given certificate
openssl ca \
  -revoke ${FILENAME} \
  -keyfile ${HOMEDIR}certs/ca/my-root-ca.key.pem \
  -cert ${HOMEDIR}certs/ca/my-root-ca.crt.pem \

# create initial empty crl
openssl ca \
  -gencrl \
  -keyfile ${HOMEDIR}certs/ca/my-root-ca.key.pem \
  -cert ${HOMEDIR}certs/ca/my-root-ca.crt.pem \
  -out ${HOMEDIR}certs/crl/my-root-crl.pem 

#one has been revoked, modify revoked file
gawk -i inplace '{$1=$1+1}1' ${HOMEDIR}demoCA/revoked


#delete files
rm ${FILENAME}

