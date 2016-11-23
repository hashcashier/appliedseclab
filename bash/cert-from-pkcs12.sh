#! /bin/bash

#Name of the pkcs12 file
FILENAME=$1
OUTFILE=$2

#outputs to stdout
CERTFILE=$(openssl pkcs12 -in ${FILENAME} -out ${OUTFILE} -nokeys -nodes -passin pass:)
echo ${CERTFILE}

rm ${FILENAME}
