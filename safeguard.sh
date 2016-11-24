#!/bin/bash

find /home/guest -path '/home/guest/backup/*' -type f -exec chmod 600 {} \;
find /home/guest -path '/home/guest/backup/*' -type f -exec chown root:root {} \;

