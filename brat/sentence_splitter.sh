#!/bin/sh
# Runs split_sentence.py to generate the sentences spans for all the files

#DIR=workspace
INDIR=$1
OUTDIR=$2

if [ ! -d "$OUTDIR" ]; then
  mkdir "$OUTDIR"
fi

for F in $INDIR/*.txt;
do
  echo "Splitting sentences of $F..."
  PREFIX=$(basename $F)
  PREFIX=${PREFIX%%.*}
  java -mx3g -cp "../corenlp/*" edu.stanford.nlp.pipeline.StanfordCoreNLP -annotators tokenize,ssplit -file "$F" -outputDirectory "$OUTDIR"
  python split_sentences.py "$OUTDIR" "$F" > "$OUTDIR/$PREFIX.sentences"
done
