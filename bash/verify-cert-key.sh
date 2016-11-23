#!/bin/bash


#Arguments:	FQDN = uid
#	 	CERTFILE = path to certificate file to check
#		KEYFILE = path to private key file to check

#Extracts the public key from both the certificate and the private key and checks for differences
#Uses tmp folder to save files

HOMEDIR="/home/imovies/appliedseclab/bash/"
FQDN=$1
CERTFILE=$2
KEYFILE=$3

#Extract from key file
openssl rsa\
  -in ${KEYFILE}\
  -pubout\
  -out "${HOMEDIR}certs/tmp/${FQDN}_test_key.pub"

#Extract from certificate
openssl x509\
  -in ${CERTFILE}\
  -pubkey\
  -noout > ${HOMEDIR}certs/tmp/${FQDN}_test_cert.pub

#Check for differences
DIFF=$(diff ${HOMEDIR}certs/tmp/${FQDN}_test_key.pub ${HOMEDIR}certs/tmp/${FQDN}_test_cert.pub)
EXIT_CODE=$?

#Remove the temporary files
rm ${HOMEDIR}certs/tmp/${FQDN}_test_key.pub ${HOMEDIR}certs/tmp/${FQDN}_test_cert.pub
rm ${KEYFILE}

#Return exit code, if 0 then they are the same
echo ${EXIT_CODE}
