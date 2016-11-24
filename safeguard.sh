#!/bin/bash

find /home/imovies -path '/home/imovies/backup/*' -exec chmod 600 {} \;
find /home/imovies -path '/home/imovies/backup/*' -exec chown root:root {} \;

