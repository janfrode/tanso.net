#! /bin/sh -

# Make sure we're at the top level of the website, where "makeall.sh" lives:
TOPLEVEL=$PWD
cd $TOPLEVEL

if test -f makeall.sh ; then
    
    find . -name "index.txt" -exec touch '{}' \;
    for i in $(find . -name "index.txt" -print) ; do cd $(dirname $i) ;  make ; cd $TOPLEVEL ; done
fi
