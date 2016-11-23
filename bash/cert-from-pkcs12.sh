#! /bin/bash

#Name of the pkcs12 file
FILENAME=$1

#outputs to stdout
openssl pkcs12 \
  -in ${FILENAME} \
  -passin pass: \
  -nokeys 
