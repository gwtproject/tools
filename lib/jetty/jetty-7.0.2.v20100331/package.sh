#!/bin/sh

# die "message"
function die() {
  echo $1 >&2
  exit 1
}

cur=$(pwd)

# update when packaging a new version
vers="7.0.2.v20100331"

if [ $# -lt 1 ] || [ $# -gt 2 ]; then
  die "Usage: $0 jetty_dist [jetty_source]"
fi

dist=$1
if [ ! -d "$dist" ]; then
  die "$dist is not an accessible directory"
fi
dist=$(cd $dist; pwd)

src=$2
if [ ! -z "$src" ] && [ ! -d "$src" ]; then
  die "$src is not an accessible directory"
fi
if [ ! -z "$src" ]; then
  src=$(cd $src; pwd)
fi

tmp=`mktemp -d -t unpack.XXXXXXXXXX` || exit 1
trap 'rm -rf $tmp' 0
cd $tmp

# subset of jars we need for GWT
jars="continuation http io security server servlet servlets util webapp websocket xml"

# license/etc files
copy="README.txt LICENSE-* about.html notice.html"

echo "Producing binary jar"
for jar in $jars; do
  jarfile=$dist/lib/jetty-$jar-$vers.jar
  echo "  unpacking $jarfile"
  jar xf $jarfile
done
rm -rf META-INF
jar cmf $cur/manifest.txt $cur/jetty-$vers.jar .
for f in $copy; do
  cp $dist/$f $cur
done

if [ ! -z "$src" ]; then
  echo "Producing source jar"
  out=$cur/jetty-$vers-src.zip
  rm -f $out
  for dir in $jars; do
    echo "  packaging source from $dir"
    (cd $src/jetty-$dir/src/main/java; zip -r -D -9 -q $out * -x '*/.svn/*')
  done
fi

exit 0
