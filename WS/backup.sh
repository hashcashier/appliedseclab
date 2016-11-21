#!/bin/bash
#to add to folder /etc/crond/cron.daily as executable
#also to do : configure ssh on backup server so that WS can ssh in (change to password auth, ssh-keygen on WS, ssh-copy-id backup, enter passwords, change back to no password auth)

PHPLOGDIR="/etc/apache2"
MYSQLLOGDIR="/var/lib/mysql/"
PAGESDIR="/var/www/"

#Send pages to backup
rsync -av -e ssh $PAGESDIR imovies@backup:/home/imovies/wsPages/

#Sned logs to backup
rsync -av -e ssh $PHPLOGDIR imovies@backup:/home/imovies/wsPhpLog/ 
rsync -ac -e ssh $MYSQLLOGDIR imovies@backup:/home/imovies/wsSQLLog/

