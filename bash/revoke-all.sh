#!/bin/bash


#Arguments: 	FQDN = uid

#Revokes all certificates beloging to user (found under certs/users/uid/*.crt.pem)
#Generates a new crl 

#This crl : certs/crl/my-root-crl.pem must be scp to WS


#name of the user
FQDN=$1

for filename in certs/users/${FQDN}/*.crt.pem; do
  echo $filename
  #revoke given certificate
  EXITCODE=$(openssl ca -cert certs/ca/my-root-ca.crt.pem -keyfile certs/ca/my-root-ca.key.pem -revoke "$filename")
  echo ${EXITCODE}
  MODIFIED=$(gawk -i inplace '{$1=$1+1}1' demoCA/revoked)
  #remove cert to avoid revoking multiple times
  rm $filename 
done

# generate new crl
openssl ca \
  -gencrl \
  -keyfile certs/ca/my-root-ca.key.pem \
  -cert certs/ca/my-root-ca.crt.pem \
  -out certs/crl/my-root-crl.pem

#modify revoked file
