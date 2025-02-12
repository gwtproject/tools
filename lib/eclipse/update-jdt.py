#!/usr/bin/env python3
"""
Usage: ./clean_jars.py <jdt version>

This script does the following:
  1) Runs Maven to copy dependencies (and sources) into a temporary directory ("./temp")
  2) Cleans/creates the output directory (whose name is given by the jdt version parameter)
  3) Copies all JAR files (and only JARs) from the temp directory to the output directory,
     preserving the subdirectory structure.
  4) Removes signature files (META-INF/*.SF and META-INF/*.RSA) from each copied JAR (using the zip command)
  5) Removes the temporary directory

Note: The bash version had a header comment that mentioned two parameters, but in fact only one
      parameter (the JDT version) is used; this same script follows that logic.
"""

import os
import sys
import shutil
import subprocess

def run_maven_commands(jdt_version, input_dir):
    """
    Run the Maven commands to copy the dependencies and sources into the temporary directory.
    """
    maven_cmd = [
        "mvn", "-f", "./dep-grab/pom.xml",
        "dependency:copy-dependencies",
        f"-Djdt.version={jdt_version}",
        f"-DoutputDirectory=.{input_dir}"
    ]
    print("Running Maven to copy dependencies...")
    subprocess.run(maven_cmd, check=True)

    maven_cmd_sources = maven_cmd + ["-Dclassifier=sources"]
    print("Running Maven to copy sources...")
    subprocess.run(maven_cmd_sources, check=True)


def clean_output_directory(output_dir):
    """
    Remove the output directory if it exists and then create it.
    """
    print(f"Cleaning/creating output directory: {output_dir}")
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)


def copy_jars(input_dir, output_dir):
    """
    Walk the input directory (which is "./temp"), and copy any file ending with .jar to the
    output directory preserving the directory structure.
    """
    print(f"Copying JAR files from: {input_dir} to: {output_dir}")
    for root, _, files in os.walk(input_dir):
        for filename in files:
            if filename.lower().endswith('.jar'):
                src = os.path.join(root, filename)
                # Get relative path from input_dir to maintain the structure.
                rel_path = os.path.relpath(src, input_dir)
                dest = os.path.join(output_dir, rel_path)
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                shutil.copy2(src, dest)


def remove_signature_files(output_dir):
    """
    For each jar file in the output directory, run 'zip -d' to remove META-INF/*.SF and META-INF/*.RSA.
    """
    print("Removing signature files (*.SF, *.RSA) from copied JARs...")
    for root, _, files in os.walk(output_dir):
        for filename in files:
            if filename.lower().endswith('.jar'):
                jar_path = os.path.join(root, filename)
                print(f"Cleaning {jar_path}")
                # Call zip -d to delete the signature files.
                # Any errors (for example, if the jar does not contain those files) are ignored.
                try:
                    subprocess.run(
                        ["zip", "-d", jar_path, "META-INF/*.SF", "META-INF/*.RSA"],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                        check=True
                    )
                except subprocess.CalledProcessError:
                    # If the zip command fails, we ignore the error.
                    pass


def main():
    # Verify that the required parameter is provided.
    if len(sys.argv) < 2:
        print("Usage: {} <jdt version>".format(sys.argv[0]))
        sys.exit(1)

    # In the original bash script, the only parameter is used as the JDT version as well as the output directory.
    jdt_version = sys.argv[1]
    input_dir = "./temp"
    output_dir = sys.argv[1]

    # 1) Run Maven commands to copy dependencies and sources.
    run_maven_commands(jdt_version, input_dir)

    # 2) Clean (or create) the output directory.
    clean_output_directory(output_dir)

    # 3) Copy all jar files from the temporary input directory to the output directory.
    copy_jars(input_dir, output_dir)

    # 4) Remove the signature files from the copied jars.
    remove_signature_files(output_dir)

    # 5) Remove the temporary input directory.
    shutil.rmtree(input_dir, ignore_errors=True)

    print(f"Done! Cleaned JARs are in: {output_dir}")

if __name__ == '__main__':
    main()
