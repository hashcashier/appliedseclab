#!/bin/bash

HOMEDIR="/home/imovies/appliedseclab/bash/"
# make directories to work from
mkdir -p ${HOMEDIR}certs/ca ${HOMEDIR}certs/crl
mkdir ${HOMEDIR}demoCA

echo "01" > ${HOMEDIR}certs/ca/my-root-ca.srl
echo "01" > ${HOMEDIR}demoCA/crlnumber
echo "00" > ${HOMEDIR}demoCA/serial
echo "0" > ${HOMEDIR}demoCA/generated
echo "0"> ${HOMEDIR}demoCA/revoked
touch ${HOMEDIR}demoCA/index.txt
touch ${HOMEDIR}demoCA/stats

# Create your very own Root Certificate Authority
openssl genrsa \
  -out ${HOMEDIR}certs/ca/my-root-ca.key.pem \
  2048

# Self-sign your Root Certificate Authority
# Since this is private, the details can be as bogus as you like
openssl req \
  -x509 \
  -new \
  -nodes \
  -key ${HOMEDIR}certs/ca/my-root-ca.key.pem \
  -days 9131 \
  -out ${HOMEDIR}certs/ca/my-root-ca.crt.pem \
  -subj "/C=CH/ST=Zurich/L=Zurich/O=iMovies/CN=iMovies CA"

