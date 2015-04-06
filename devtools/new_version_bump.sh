#!/bin/bash

YEAR=$(date +'%Y')

echo -n "Type version to apply: "
read ver

# Replace the copyright and version number in every .py file header
if [ -n "$ver" ]; then
    perl -p -i -e "s/(?<=:Copyright: \(c\))[0-9]{4}(?= by Pablo)/$YEAR/g" `find ../ -name '*.py'`
    perl -p -i -e "s/(?<=:Version: ).+/$ver/g" `find ../ -name '*.py'`
    echo "Headers of jgrampro files are now set at '$ver' version and the year '$YEAR'"
else
    echo "Version not provided. No changes were done."
fi
