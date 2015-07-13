#!/bin/sh
# Runs linnaeus with default settings over the text files to extract the species

#DIR=workspace
INDIR="$1"
OUTDIR="$2"

if [ ! -d "$OUTDIR" ]; then
  mkdir "$OUTDIR"
fi

echo "Running Linnaeus on the text files at $INDIR"
java -Xmx6G -jar ../linnaeus-2.0.jar --properties ../linnaeus.conf --textDir $INDIR --outDir $OUTDIR

# Remove the first line of each output file
# because it is a header row
for F in $OUTDIR/*.tags
do
  NAME=${F#.*}.species
  awk '{ if(!$NR==1) print $0; }' $F > "$NAME.temp"
  python postprocess_species.py "$OUTDIR" "$NAME.temp" | sort -Vu > "$NAME"
  rm $F $NAME.temp
done
