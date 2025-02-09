#!/usr/bin/env bash
#
# Usage: ./clean-jars.sh <inputDir> <outputDir>
#
# 1) Cleans/creates <outputDir>
# 2) Copies all JARs (and only JARs) from <inputDir> to <outputDir>, preserving directory structure
# 3) Removes META-INF/*.SF and META-INF/*.RSA files in-place from the copied JARs

set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "Usage: $0 <inputDir> <outputDir>"
  exit 1
fi

INPUT_DIR="$1"
OUTPUT_DIR="$2"

# 1) Clean/create output directory
echo "Cleaning/creating output directory: $OUTPUT_DIR"
rm -rf "$OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR"

# 2) Copy all JAR files from input to output, preserving subdir structure
echo "Copying JAR files from: $INPUT_DIR to: $OUTPUT_DIR"
while IFS= read -r -d '' jar; do
  # Remove the leading "$INPUT_DIR/" part to get the relative path
  relPath="${jar#$INPUT_DIR/}"
  outJar="$OUTPUT_DIR/$relPath"

  # Make sure the subdirectory structure exists
  mkdir -p "$(dirname "$outJar")"

  # Copy the JAR
  cp "$jar" "$outJar"
done < <(find "$INPUT_DIR" -type f -name '*.jar' -print0)

# 3) Remove signature files from the copied JARs
echo "Removing signature files (*.SF, *.RSA) from copied JARs..."
find "$OUTPUT_DIR" -type f -name '*.jar' | while read -r jar; do
  echo "Cleaning $jar"
  # 'zip -d' will remove these entries from the jar
  zip -d "$jar" "META-INF/*.SF" "META-INF/*.RSA" 2>/dev/null || true
done

echo "Done! Cleaned JARs are in: $OUTPUT_DIR"
