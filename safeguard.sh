#!/bin/bash

find . -path 'backup/*' -type f -exec chmod 600 {} \;
find . -path 'backup/*' -type f -exec chown root:root {} \;

