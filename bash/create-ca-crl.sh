#!/bin/bash

# create crl from demoCA/index.txt file
openssl ca \
  -gencrl \
  -keyfile certs/ca/my-root-ca.key.pem \
  -cert certs/ca/my-root-ca.crt.pem \
  -out certs/crl/my-root-crl.pem 

