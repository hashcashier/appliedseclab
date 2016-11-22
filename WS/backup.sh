#!/bin/bash
#to add to folder /etc/crond/cron.daily as executable
#also to do : configure ssh on backup server so that WS can ssh in (change to password auth, ssh-keygen on WS, ssh-copy-id backup, enter passwords, change back to no password auth)

PHPLOGDIR="/etc/apache2"
MYSQLLOGDIR="/var/lib/mysql/"
PAGESDIR="/var/www/"
BACKUP="192.168.2.99"

#Send pages to backup
rsync -av -e ssh $PAGESDIR imovies@$BACKUP:/home/imovies/wsPages/

#Sned logs to backup
rsync -av -e ssh $PHPLOGDIR imovies@$BACKUP:/home/imovies/wsPhpLog/ 
rsync -av -e ssh $MYSQLLOGDIR imovies@$BACKUP:/home/imovies/wsSQLLog/

