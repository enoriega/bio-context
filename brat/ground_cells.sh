#!/bin/bash
# Grounds species mentions from context a custom unique ID
# if it is not detected

# Where the context file annotations are
DIR=$1
DICT="cells_dict.pickle"

# We will work on all the context annotations to provide global ids
cat $DIR/*.context_features | grep -e Cell-Line -e Cell-Type | awk -F':' '{ print $4 }' | sort -u > mentions.txt

# Build the dict with ids
#python ground_context_cells.py -dict mentions.txt > $DICT

# Ground species
for F in $DIR/*.context_features
do
  mv "$F" "$F.temp"
  python ground_context_cells.py -ground "$F.temp" "$DICT" > "$F"
  rm "$F.temp"
done

# Cleanup
rm mentions.txt
