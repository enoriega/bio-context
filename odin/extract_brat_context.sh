#!/bin/sh

DIR='brat_sof'
TSVDIR='tsv'

# Iterate through each stand off file
for F in $DIR/*.ann
do
  #Extract the text-bound id of the Context-of relations
  IDS=$(sed -n '/ContextOf/ {s/.\+Context:\(T[0-9]\+\)/\1/p}' $F)
  for ID in $IDS
  do
    LINE=$(grep "^$ID\t" $F | sort -u)
    FILE=$(echo "$LINE" | awk '{print $2}')
    TEXT=$(echo "$LINE" | awk -F'\t' '{print $3}')

    # This is to add the entries to the NER
    echo $TEXT >> $FILE.context
  done
done

for F in *.context
do
  sort -u $F > $F.txt
  rm $F
done
