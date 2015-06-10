#!/usr/bin/python2.4
# update-jdt.py
#
# This script is used to massage a JDT jar from Eclipse
# for inclusion in the GWT tools repository.
# It strips out files that are not needed and adds a version.txt
# file.
#
# Run it as:
#
# python update-jdt.py jarfile sourcefile

import re
import sys
import zipfile

# White listing
jarWhitelist = [
    "about.html",
    "org/eclipse/jdt/core/compiler",
    "org/eclipse/jdt/internal/compiler",
    "org/eclipse/jdt/internal/core/util"
]

def whitelistAllows(filename):
    for start in jarWhitelist:
        if filename.startswith(start):
            return True
    return False


# Parse arguments
if len(sys.argv) != 3:
    print "Usage: python update-jdt.py org.eclipse.jdt.core_N.N.N.v_NNN_RNNx.jar org.eclipse.jdt.core.source_N.N.N.v_NNN_RNNx.jar"
    sys.exit(1)

jdtjar = sys.argv[1]
srcjar = sys.argv[2]

print "JDT jar: " + jdtjar
print "source jar: " + srcjar


# extract versions from the names, and make sure they match
versionOfJarPattern = re.compile(r"org\.eclipse\.jdt\.core(\.source)?_(.*)\.jar")
def versionOfJar(jarname):
    match = versionOfJarPattern.match(jarname)
    if match == None:
        return ""
    else:
        return match.group(2)

version = versionOfJar(jdtjar)
srcversion = versionOfJar(srcjar)

if version == None or srcversion == None:
    print "Cannot determine the version number of these jars."
    sys.exit(2)

if version != srcversion:
    print "The version of the two jars is inconsistent (" + version1 + " vs. " + version2
    sys.exit(2)

print "long version: " + version

shortVersionPattern = re.compile(r"([0-9]+\.[0-9]+\.[0-9]+)\.v.*")
shortVersion = shortVersionPattern.match(version).group(1)

print "short version: " + shortVersion



# build jars for GWT
def filterjar(injarname, outjarname):
    print "writing " + outjarname + "..."

    outzip = zipfile.ZipFile(outjarname, mode='w')
    inzip = zipfile.ZipFile(injarname, mode='r')

    for info in inzip.infolist():
        if whitelistAllows(info.filename):
            data = inzip.read(info.filename)
            outinfo = zipfile.ZipInfo(filename=info.filename,
                                      date_time=info.date_time)
            outinfo.external_attr = 0600 << 16L #fixup permissions
            outinfo.compress_type = zipfile.ZIP_DEFLATED
            outzip.writestr(outinfo, data)

    inzip.close()
    outzip.close()

jdtforgwt = "jdt-" + shortVersion + ".jar"
srcforgwt = "jdt-" + shortVersion + "-src.zip"

filterjar(jdtjar, jdtforgwt)
filterjar(srcjar, srcforgwt)


# add version.txt
jdtzip = zipfile.ZipFile(jdtforgwt, "a")
jdtzip.writestr(zipfile.ZipInfo(filename="org/eclipse/jdt/version.txt"),
                "version " + version + "\n")
jdtzip.close()
