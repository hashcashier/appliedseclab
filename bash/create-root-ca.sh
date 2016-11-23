#!/bin/bash

# make directories to work from
mkdir -p certs/ca certs/crl
mkdir demoCA

echo "01" > certs/ca/my-root-ca.srl
echo "01" > demoCA/crlnumber
echo "01" > demoCA/serial
touch demoCA/index.txt

# Create your very own Root Certificate Authority
openssl genrsa \
  -out certs/ca/my-root-ca.key.pem \
  2048

# Self-sign your Root Certificate Authority
# Since this is private, the details can be as bogus as you like
openssl req \
  -x509 \
  -new \
  -nodes \
  -key certs/ca/my-root-ca.key.pem \
  -days 9131 \
  -out certs/ca/my-root-ca.crt.pem \
  -subj "/C=CH/ST=Zurich/L=Zurich/O=iMovies/CN=iMovies CA"

