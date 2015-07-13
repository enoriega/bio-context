''' Set up dataframes to query statistics from event and context labels '''
import pandas as pd
import numpy as np
import glob, re, os
import os.path as path
import matplotlib.pyplot as plt
from sklearn.feature_extraction import DictVectorizer


### Load featues

lines, species, cells, genes, relations = [], [], [], [], []
context_ann, event_ann = [], []

# Get the document prefixes
entries = {e.split('.')[0] for e in os.listdir('output')}

for e in entries:
    # get the lines
    with open(path.join('workspace', e+'.sentences')) as f:
        lines.extend([{'doc':e, 'num':int(num), 'start':int(start), 'end':int(end),
         'text':text} for num, start, end, text in [l[:-1].split('\t', 3) for l in f]])

    # Get species
    with open(path.join('workspace', e+'.species')) as f:
        species.extend([{'doc':e, 'line':int(num), 'location':int(location), 'text':text} for
         num, location, text in [l[:-1].split('\t', 2) for l in f]])

    # Get cells
    with open(path.join('workspace', e+'.cells')) as f:
        cells.extend([{'doc':e, 'line':int(num), 'location':int(location), 'text':text} for
         num, location, text in [l[:-1].split('\t', 2) for l in f]])

    # Get genes
    with open(path.join('workspace', e+'.genes')) as f:
        genes.extend([{'doc':e, 'line':int(num), 'location':int(location), 'text':text} for
         num, location, text in [l[:-1].split('\t', 2) for l in f]])

    # Get relations
    with open(path.join('workspace', e+'.txt.sentences.relations')) as f:
        relations.extend([{'doc':e, 'line':int(num), 'first':first,
         'second':second, 'type':t} for
         num, first, second, t in [l[:-1].split('\t') for l in f]])


    # Load context annotations
    with open(path.join('output', e+'.context_features')) as f:
        for l in f:
            id, line, kind, text = l[:-1].split(':')
            context_ann.append({
                'doc':e,
                'event':int(id),
                'line':int(line),
                'type':kind,
                'text':text
            })

    # Load event annotations
    with open(path.join('output', e+'.events_features')) as f:

        chunks = []
        current = []

        for l in f:
            l = l[:-1]
            if l == '':
                chunks.append(current)
                current = []
            else:
                current.append(l)

        chunks.append(current)

        for chunk in chunks:
            event_ann.append({
                'doc':e,
                'id':int(chunk[0]),
                'type':chunk[1],
                'line':int(chunk[2]),
                'participants':chunk[6] if len(chunk) >= 6 else None
            })


# Build the dataframes
lines = pd.DataFrame(lines)
species = pd.DataFrame(species)
cells = pd.DataFrame(cells)
genes = pd.DataFrame(genes)
relations = pd.DataFrame(relations)
context = pd.DataFrame(context_ann)
events = pd.DataFrame(event_ann)

# Sort them
species.sort(['doc', 'line', 'location', 'text'], axis=0, inplace=True)
cells.sort(['doc', 'line', 'location', 'text'], axis=0, inplace=True)
genes.sort(['doc', 'line', 'location', 'text'], axis=0, inplace=True)
relations.sort(['doc', 'line', 'type', 'first', 'second'], axis=0, inplace=True)
context.sort(['doc', 'line', 'type'], axis=0, inplace=True)
events.sort(['doc', 'line', 'type'], axis=0, inplace=True)

documents = lines.doc.drop_duplicates()



def detailed_counts():
    for d in documents:
        print d
        print
        print "Context annotation distribution:"
        print context[context.doc == d].type.value_counts()
        print
        print "Number of features:"
        print "Species:\n%s\nTotal: %i" % (species[species.doc == d].text.value_counts(), species[species.doc == d].text.value_counts().sum())
        print
        print "Cells:\n%s\nTotal: %i" % (cells[cells.doc == d].text.value_counts(), cells[cells.doc == d].text.value_counts().sum())
        print
        print "Gene products:\n%s\nTotal: %i" % (genes[genes.doc == d].text.value_counts(), genes[genes.doc == d].text.value_counts().sum())
        print
        print "Relations:\n%s\nTotal: %i" % (relations[relations.doc == d].type.value_counts(), relations[relations.doc == d].type.value_counts().sum())
        print
        print

def summarized_counts():
    for d in documents:
        print d
        print
        print "Context annotation distribution:"
        print context[context.doc == d].type.value_counts()
        print
        print "Number of features:"
        print
        print "Species: %i" % (species[species.doc == d].text.value_counts().sum())
        print "Cells: %i" % (cells[cells.doc == d].text.value_counts().sum())
        print "Gene products: %i" % (genes[genes.doc == d].text.value_counts().sum())
        print
        print "Relations:\n%s\nTotal: %i" % (relations[relations.doc == d].type.value_counts(), relations[relations.doc == d].type.value_counts().sum())
        print
        print

def histogram():
    ix = np.arange(4)
    plt.ion()
    for d in documents:
        bars = (species[species.doc == d].shape[0], cells[cells.doc == d].shape[0],
        genes[genes.doc == d].shape[0], relations[relations.doc == d].shape[0])
        plt.figure()
        plt.bar(ix, bars)
        plt.title(d)
        plt.xlabel('Feature Type')
        plt.ylabel('Count')
        plt.xticks(ix + 0.5, ('SP', 'CELL', 'GENE', 'REL'))
        plt.show()
    plt.ioff()
