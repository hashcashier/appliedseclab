#!/bin/bash
adduser guest
mkdir /home/guest/.ssh/
chown guest /home/guest/.ssh/authorized_keys
chgrp guest /home/guest/.ssh/authorized_keys

mkdir /home/guest/backup/caCerts/
mkdir /home/guest/backup/caLogs/
mkdir /home/guest/backup/caConfigs/
mkdir /home/guest/backup/apacheLogs/
mkdir /home/guest/backup/sqlLogs/
mkdir /home/guest/backup/db/

chown guest /home/guest/backup/*
chgrp guest /home/guest/backup/*

chmod +t /home/guest/backup
chmod +t /home/guest/backup/*

cp safeguard /home/guest/safeguard
chown root /home/guest/safeguard
chmod a+x /home/guest/safeguard
chmod +s /home/guest/safeguard

cp safeguard.sh /home/guest/safeguard.sh
chown root /home/guest/safeguard.sh
chmod og-rwx /home/guest/safeguard.sh
chmod u+x /home/guest/safeguard.sh
