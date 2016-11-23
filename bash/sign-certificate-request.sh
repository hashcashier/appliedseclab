#!/bin/bash

#Arguments: 	FQDN = uid

#Takes the lastest unsigned csr and signs it with serial number SERIAL, updates the cerial number, signs with CA certificate and key

#Then deletes the csr


FQDN="$1"
SERIAL=$(cat demoCA/serial)

# Sign the request from Server with your Root CA
openssl x509 \
  -req -in "certs/tmp/${FQDN}.csr.pem" \
  -CA "certs/ca/my-root-ca.crt.pem" \
  -CAkey "certs/ca/my-root-ca.key.pem" \
  -CAserial "demoCA/serial"\
  -out "certs/users/${FQDN}/${SERIAL}.crt.pem" \
  -days 9131

#remove csr file
rm certs/tmp/${FQDN}.csr.pem

#writes new Serial number to stdout
echo ${SERIAL}

