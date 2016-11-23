#!/bin/bash

HOMEDIR="/home/imovies/appliedseclab/bash/"

echo $(cat ${HOMEDIR}demoCA/generated) > ${HOMEDIR}demoCA/stats
echo $(cat ${HOMEDIR}demoCA/revoked) >> ${HOMEDIR}demoCA/stats 
echo $(cat ${HOMEDIR}demoCA/serial) >> ${HOMEDIR}demoCA/stats 

