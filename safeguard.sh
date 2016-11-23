#!/bin/bash

for filename in /home/guest/backup/*/*; do
  chown root $filename
  chmod 600 $filename
done
