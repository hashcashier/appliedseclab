#!/bin/bash


#Arguments:	FQDN = uid
#	 	CERTFILE = path to certificate file to check
#		KEYFILE = path to private key file to check

#Extracts the public key from both the certificate and the private key and checks for differences
#Uses tmp folder to save files


FQDN=$1
CERTFILE=$2
KEYFILE=$3

#Extract from key file
openssl rsa\
  -in ${KEYFILE}\
  -pubout\
  -out "certs/tmp/${FQDN}_test_key.pub"

#Extract from certificate
openssl x509\
  -in ${CERTFILE}\
  -pubkey\
  -noout > certs/tmp/${FQDN}_test_cert.pub

#Check for differences
DIFF=$(diff certs/tmp/${FQDN}_test_key.pub certs/tmp/${FQDN}_test_cert.pub)
EXIT_CODE=$?

#Remove the temporary files
rm certs/tmp/${FQDN}_test_key.pub certs/tmp/${FQDN}_test_cert.pub

#Return exit code, if 0 then they are the same
echo ${EXIT_CODE}
