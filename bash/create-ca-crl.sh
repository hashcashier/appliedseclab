#!/bin/bash

HOMEDIR="/home/imovies/appliedseclab/bash/"

# create crl from demoCA/index.txt file
openssl ca \
  -gencrl \
  -keyfile ${HOMDEIR}certs/ca/my-root-ca.key.pem \
  -cert ${HOMEDIR}certs/ca/my-root-ca.crt.pem \
  -out ${HOMEDIR}certs/crl/my-root-crl.pem 

