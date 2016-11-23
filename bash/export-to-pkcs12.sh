#!/bin/bash

#Argments:	FQDN = uid

#Takes the current user/serial number's keyfile and certificate file and exports to pkcs12 format
#Saves output in certs/users/uid/uid.serial_num.pfx 

#The file certs/user/uid/uid.serial_num.pfx is to be scp to the WS 


FQDN=$1
SERIAL=$2

openssl pkcs12 \
  -export \
  -inkey "certs/users/${FQDN}/${SERIAL}.key.pem" \
  -in "certs/users/${FQDN}/${SERIAL}.crt.pem" \
  -out "certs/users/${FQDN}/${FQDN}.${SERIAL}.pfx" \
  -passout pass:
