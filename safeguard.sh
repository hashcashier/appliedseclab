#!/bin/bash

find /home/guest -path '/home/guest/backup/*' -exec chmod 600 {} \;
find /home/guest -path '/home/guest/backup/*' -exec chown root:root {} \;

