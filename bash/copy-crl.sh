#!/bin/bash
# Use CRL
FNAME=`openssl crl -hash -noout -in /var/www/html/bash/client/crl.pem`
cp /var/www/html/bash/client/crl.pem /var/www/crl/$FNAME &&
rm /var/www/crl/$FNAME.r0;
ln -s /var/www/crl/$FNAME /var/www/crl/$FNAME.r0 &&
sudo /var/www/graceful;
