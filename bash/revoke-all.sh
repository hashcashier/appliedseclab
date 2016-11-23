#!/bin/bash


#Arguments: 	FQDN = uid

#Revokes all certificates beloging to user (found under certs/users/uid/*.crt.pem)
#Generates a new crl 

#This crl : certs/crl/my-root-crl.pem must be scp to WS

HOMEDIR="/home/imovies/appliedseclab/bash/"

#name of the user
FQDN=$1

for filename in ${HOMEDIR}certs/users/${FQDN}/*.crt.pem; do
  echo $filename
  #revoke given certificate
  EXITCODE=$(openssl ca -cert ${HOMEDIR}certs/ca/my-root-ca.crt.pem -keyfile ${HOMEDIR}certs/ca/my-root-ca.key.pem -revoke "$filename")
  MODIFIED=$(gawk -i inplace '{$1=$1+1}1' ${HOMEDIR}demoCA/revoked)
  #remove cert to avoid revoking multiple times
done

# generate new crl
openssl ca \
  -gencrl \
  -keyfile ${HOMEDIR}certs/ca/my-root-ca.key.pem \
  -cert ${HOMEDIR}certs/ca/my-root-ca.crt.pem \
  -out ${HOMEDIR}certs/crl/my-root-crl.pem
