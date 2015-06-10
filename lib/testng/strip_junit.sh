#/bin/bash
#
# Shell script to divorce junit from testNG

if [ $# != 2 ]; then
  echo "usage: $0 jarfile newfile"
  exit 1
fi

set -e 
mkdir tmp
cd tmp
jar xf ../$1
rm -rf junit*
rm -rf org/junit*
jar cf ../$2 *
cd ..
rm -rf tmp

