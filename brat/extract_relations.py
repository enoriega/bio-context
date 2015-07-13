''' Looks for relations of the types of interest between entities on each sentence '''

import sys, glob, os
import pandas as pd
import itertools as it

# TODO: Do something to ignore the methods section

pworkspace  = sys.argv[1]

# Keywords
keywords = ['for', 'of', 'to', 'from', 'at', 'in', 'on']

# Get the list of documents from the workspace dir

prefixes = set(p.split('.')[0] for p in glob.iglob(os.path.join(pworkspace, '*')))

for p in prefixes:
    psentences = p + '.sentences'
    #pspecies = p + '.tags.species'
    pspecies = p + '.species'
    pcells = p + '.cells'
    pgenes = p + '.genes'

    sentences = {}
    with open(psentences) as f:
        for line in f:
            line = line[:-1]
            num, start, end, text = line.split('\t')
            sentences[int(num)] = text


    species = []
    with open(pspecies) as f:
        for line in f:
            line = line[:-1]
            #ncbi, doc, position, num, text = line.split('\t')
            num, position, text = line.split('\t')
            #species.append({'line':int(num), 'position':int(position), 'text':ncbi})
            species.append({'line':int(num), 'position':int(position), 'text':text})

    species = pd.DataFrame(species, columns=['line', 'position', 'text'])
    if len(species) > 0:
        species.set_index('line', inplace=True)
        species = species.groupby(level=0)

    cells = []
    with open(pcells) as f:
        for line in f:
            line = line[:-1]
            num, position, text = line.split('\t')
            cells.append({'line':int(num), 'position':int(position), 'text':text})
    cells = pd.DataFrame(cells, columns=['line', 'position', 'text'])
    if len(cells) > 0:
        cells.set_index('line', inplace=True)
        cells = cells.groupby(level=0)

    genes = []
    with open(pgenes) as f:
        for line in f:
            line = line[:-1]
            num, position, text = line.split('\t')
            genes.append({'line':int(num), 'position':int(position), 'text':text})
    genes = pd.DataFrame(genes, columns=['line', 'position', 'text'])
    if len(genes) > 0:
        genes.set_index('line', inplace=True)
        genes = genes.groupby(level=0)

    # Now do cross products
    for ix in sentences:
        # species X cells
        if len(species) > 0 and species.groups.has_key(ix)\
         and len(cells) > 0 and cells.groups.has_key(ix):
            s = species.get_group(ix).values.tolist()
            c = cells.get_group(ix).values.tolist()

            entities = s + c

            # Sort them
            entities = sorted(entities, key=lambda x: x[0])

            # Tokenize the sentence
            sentence = sentences[ix]

            # Iterate per pairs of entities
            for i in xrange(1, len(entities)):
                first, second = entities[i-1], entities[i]

                # If both are of the same kind, then move on
                if (first in s and second in s) or (first in c and second in c):
                    continue

                extract = sentence[first[0]:second[0]]
                tokens = [t.strip().lower() for t in extract.split()]

                for kw in keywords:
                    if kw in tokens:
                        #print '(%s, %s, %s, %s)' % (first, second, kw, sentence)
                        with open(p + '.txt.sentences.relations', 'w') as f:
                            f.write('%i\t%s\t%s\t%s\n' % (ix, first[1], second[1], kw))


        # species X genes
        if len(species) > 0 and species.groups.has_key(ix)\
         and len(genes) > 0 and genes.groups.has_key(ix):
            s = species.get_group(ix).values.tolist()
            g = genes.get_group(ix).values.tolist()

            entities = s + g

            # Sort them
            entities = sorted(entities, key=lambda x: x[0])

            # Tokenize the sentence
            sentence = sentences[ix]

            # Iterate per pairs of entities
            for i in xrange(1, len(entities)):
                first, second = entities[i-1], entities[i]

                # If both are of the same kind, then move on
                if (first in s and second in s) or (first in g and second in g):
                    continue

                extract = sentence[first[0]:second[0]]
                tokens = [t.strip().lower() for t in extract.split()]

                for kw in keywords:
                    if kw in tokens:
                        #print '(%s, %s, %s, %s)' % (first, second, kw, sentence)
                        with open(p + '.txt.sentences.relations', 'a') as f:
                            f.write('%i\t%s\t%s\t%s\n' % (ix, first[1], second[1], kw))

        # cells X cells
        if len(cells) > 0 and cells.groups.has_key(ix):
            c = cells.get_group(ix).values.tolist()

            entities = c

            # Sort them
            entities = sorted(entities, key=lambda x: x[0])

            # Tokenize the sentence
            sentence = sentences[ix]

            # Iterate per pairs of entities
            for i in xrange(1, len(entities)):
                first, second = entities[i-1], entities[i]

                extract = sentence[first[0]:second[0]]
                tokens = [t.strip().lower() for t in extract.split()]

                for kw in keywords:
                    if kw in tokens:
                        #print '(%s, %s, %s, %s)' % (first, second, kw, sentence)
                        with open(p + '.txt.sentences.relations', 'a') as f:
                            f.write('%i\t%s\t%s\t%s\n' % (ix, first[1], second[1], kw))

        # cells X genes
        if len(cells) > 0 and cells.groups.has_key(ix)\
         and len(genes) > 0 and genes.groups.has_key(ix):
            c = cells.get_group(ix).values.tolist()
            g = genes.get_group(ix).values.tolist()

            entities = c + g

            # Sort them
            entities = sorted(entities, key=lambda x: x[0])

            # Tokenize the sentence
            sentence = sentences[ix]

            # Iterate per pairs of entities
            for i in xrange(1, len(entities)):
                first, second = entities[i-1], entities[i]

                # If both are of the same kind, then move on
                if (first in s and second in s) or (first in c and second in c):
                    continue

                extract = sentence[first[0]:second[0]]
                tokens = [t.strip().lower() for t in extract.split()]

                for kw in keywords:
                    if kw in tokens:
                        #print '(%s, %s, %s, %s)' % (first, second, kw, sentence)
                        with open(p + '.txt.sentences.relations', 'a') as f:
                            f.write('%i\t%s\t%s\t%s\n' % (ix, first[1], second[1], kw))
