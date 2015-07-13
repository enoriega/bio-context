#!/bin/sh
# Puts all together

OUTDIR="output"
INDIR="data"
WORKSPACE="workspace"
CELLS_DICT="cells_dict.pickle"
GENES_DICT="genes_dict.pickle"
SPECIES_DICT="species_dict.pickle"
# Avoid time-consuming NLP processing. Set to true only if the processed files already exist
FAST=true

if [ ! -d "$OUTDIR" ]; then
  echo "Creating output directory \"$OUTDIR\"..."
  mkdir "$OUTDIR"
fi

if [ "$FAST" = false ];
then
  # Split sentences of the text files
  echo "Splitting sentences of the data set"
  ./sentence_splitter.sh "$INDIR" "$WORKSPACE"

  # Run Linnaeus
  #echo "Running species NER"
  #./species_ner.sh "$INDIR" "$WORKSPACE"
fi

# Run the species NER
echo "Running species NER"
./species_ner_light.sh "$WORKSPACE" "$SPECIES_DICT"

#  Run cell-type/tissue-type NER
#  Run cell lines NER
echo "Running cells NER"
./cells_ner.sh "$WORKSPACE" "$CELLS_DICT"

# Run gene products ner
echo "Running genes NER"
./genes_ner.sh "$WORKSPACE" "$GENES_DICT"

echo "Extracting relations between mentions"
python extract_relations.py "$WORKSPACE"

# Parse the annotation files
for F in $INDIR/*.ann; do
  PREFIX=$(basename $F)
  CONTEXT="$OUTDIR/${PREFIX%%.*}.context_features"
  EVENTS="$OUTDIR/${PREFIX%%.*}.events_features"

  echo "Parsing context annotations from $F..."
  python parse_latent.py $F > $CONTEXT
  echo "Parsing event annotations from $F..."
  python parse_obs.py $F > $EVENTS

  echo "Writing NER features for $F..."
  # Species
  #SENTENCES=

done

#Ground/Cluster the NEs in the feature files
./ground_species.sh "$OUTDIR"
./ground_cells.sh "$OUTDIR"

# Postproces the feature files
for F in $INDIR/*.ann; do
  PREFIX=$(basename $F)
  CONTEXT="$OUTDIR/${PREFIX%%.*}.context_features"
  EVENTS="$OUTDIR/${PREFIX%%.*}.events_features"

  echo "Postprocessing features of $F..."
  python postprocess.py "$WORKSPACE" "$CONTEXT" "$EVENTS"
done
