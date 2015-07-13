#!/bin/bash
# Grounds species mentions from context with Linnaeus or a custom unique ID
# if it is not detected

# Where the context file annotations are
DIR=$1
DICT="species_dict.txt"

# We will work on all the context annotations to provide global ids
cat $DIR/*.context_features | grep Main-Species | awk -F':' '{ print $4 }' | sort -u > mentions.txt

# Build the dict with ids
python ground_context_species.py -dict mentions.txt > $DICT

# Ground species
for F in $DIR/*.context_features
do
  mv "$F" "$F.temp"
  python ground_context_species.py -ground "$F.temp" "$DICT" > "$F"
  rm "$F.temp"
done

# Cleanup
rm "$DICT"
rm mentions.txt
