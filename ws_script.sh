#!/bin/bash

cp backup_ws /etc/cron.hourly/backup
rm /etc/cron.daily/backup
chmod a+x /etc/cron.hourly/backup
