#!/bin/sh
# Scans the text from our species dictionary and outputs a file with the matches

#DIR=workspace
WORKSPACE="$1"
DICT="$2"

if [ ! -d "$WORKSPACE" ]; then
  mkdir "$WORKSPACE"
fi

# Remove the first line of each output file
# because it is a header row
for F in $WORKSPACE/*.sentences
do
  NAME=${F%%.*}.species
  python detect_species.py "$F" "$DICT" | sort -Vu > "$NAME"

done