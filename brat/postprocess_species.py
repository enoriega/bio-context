''' Gets the sentence of each species mention among other postprocessing '''
import sys, os
from utils import *

fspecies = sys.argv[2]
fworkspace = sys.argv[1]

# This is the prefix of the files for the given document
prefix = fspecies.split('/')[-1]
prefix = '.'.join(prefix.split('.')[:-3])

# Load the sentences offsets
sentences_spans = {}
with open(os.path.join(fworkspace, prefix + '.txt.sentences')) as f:
    for line in f:
        ix, start, end, text = line.split('\t')
        sentences_spans[int(ix)] = (int(start), int(end))

with open(fspecies) as f:
    for line in f:
        tokens = line.split('\t')
        interval = (int(tokens[2]), int(tokens[3]))

        sentence = get_sentence(interval, sentences_spans)

        print '%s\t%s\t%s\t%s\t%s' % (tokens[0], tokens[1], interval[0], sentence, tokens[4])
