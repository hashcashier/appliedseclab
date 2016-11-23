#!/bin/bash

echo $(cat demoCA/generated) > demoCA/stats
echo $(cat demoCA/revoked) >> demoCA/stats 
echo $(cat demoCA/serial) >> demoCA/stats 

