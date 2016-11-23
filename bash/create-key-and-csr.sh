#!/bin/bash

# Change to be whatever
FQDN="$1"
EMAIL="$2"
ADMIN="$3"
SERIAL=$(cat demoCA/serial)

# make directories to work from
mkdir -p certs/{users,tmp}

# Create Certificate for this domain,
mkdir -p "certs/users/${FQDN}"
openssl genrsa \
  -out "certs/users/${FQDN}/${SERIAL}.key.pem" \
  2048

# Create the CSR
openssl req -new \
  -key "certs/users/${FQDN}/${SERIAL}.key.pem" \
  -out "certs/tmp/${FQDN}.csr.pem" \
  -subj "/C=CH/ST=Zurich/L=Zurich/O=iMovies/OU=${ADMIN}/CN=${FQDN}/emailAddress=${EMAIL}"

#Sign the request from with your root CA
openssl x509\
  -req -in "certs/tmp/${FQDN}.csr.pem" \
  -CA "certs/ca/my-root-ca.crt.pem"\
  -CAkey "certs/ca/my-root-ca.key.pem" \
  -out "certs/users/${FQDN}/${SERIAL}.crt.pem" \
  -days 9131

#remove csr file
rm certs/tmp/${FDQN}.csr.pem

#writes corresponding serial number to stdout
echo ${SERIAL}
