#!/bin/bash

YEAR=$(date +'%Y')

# Replace the copyright and version number in every .py file header
if [ $# == 1 ]; then
    perl -p -i -e "s/(?<=:Copyright: \(c\))[0-9]{4}(?= by Pablo)/$YEAR/g" `find ./ -name '../*.py'`
    perl -p -i -e "s/(?<=:Version: ).+/$1/g" `find ./ -name '../*.py'`
else
    echo 'You should provide only 1 argument, the version to apply to the files'
fi
