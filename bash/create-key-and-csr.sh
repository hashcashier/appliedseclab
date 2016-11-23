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
