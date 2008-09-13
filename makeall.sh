#! /bin/sh -

find . -name "index.txt" -exec touch '{}' \;
for i in $(find . -name "index.txt" -print) ; do cd $(dirname $i) ;  make ; cd /var/www/html/ ; done
