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
  openssl ca -revoke $filename -keyfile certs/ca/my-root-ca.key.pem -cert certs/ca/my-root-ca.crt.pem 
done

# generate new crl
openssl ca \
  -gencrl \
  -keyfile certs/ca/my-root-ca.key.pem \
  -cert certs/ca/my-root-ca.crt.pem \
  -out certs/crl/my-root-crl.pem 
