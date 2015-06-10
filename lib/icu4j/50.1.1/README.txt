Built like this:

mkdir tmp
cd tmp
svn co http://source.icu-project.org/repos/icu/icu4j/tags/release-50-1-1 .
ant jar icu4jSrcJar releaseCLDR
cp main/shared/licenses/*.html icu4j*.jar release_cldr/utilities*.jar ..
