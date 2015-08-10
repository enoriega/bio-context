import glob
import pandas as pd
import numpy as np
import itertools as it
import matplotlib
import matplotlib.pyplot as plt
from collections import defaultdict
from sklearn.feature_extraction import DictVectorizer
from sklearn.cluster import AffinityPropagation

# Necessary to work in OS X

def parse_files(dir):
    ''' Parsed the TSV files generated from ODIN into pandas' data frames '''

    entities = {}
    for ep in glob.iglob('%s/*.entities' % dir):
        try:
            entities[ep.split('.')[0].replace(dir + '/', '')] = pd.read_csv(ep, delimiter='\t')
        except:
            print 'Problem parsing %s' % ep

    relations = {}
    for ep in glob.iglob('%s/*.relations' % dir):
        try:
            relations[ep.split('.')[0].replace(dir + '/', '')] = pd.read_csv(ep, delimiter='\t')
        except:
            print 'Problem parsing %s' % ep

    lines = {}
    for ep in glob.iglob('%s/*.lines' % dir):
        try:
            lines[ep.split('.')[0].replace(dir + '/', '')] = pd.read_csv(ep, delimiter='\t')
        except:
            print 'Problem parsing %s' % ep

    return entities, relations, lines

if __name__ == '__main__':

    print "Parsing files"
    entities, relations, lines = parse_files('tsv')

    print "Building feature vectors"
    entity_dicts, relation_dicts = defaultdict(dict), defaultdict(dict)

    ## Count entities #########################################
    # Make a large entity frame
    lent = pd.concat(entities)

    # Remove the non-grounded entities
    lent = lent[lent['Grounded ID'] != 'uniprot:UNRESOLVED ID']

    # Get the entity counts
    def make_ent_dicts(frame):
        features = defaultdict(int)
        def inc(series):
            features[series['Grounded ID']] += 1
        frame.apply(inc, axis=1)
        return features

    for name, frame in lent.groupby('Paper ID'):
        entity_dicts[name] = make_ent_dicts(frame)
    ###########################################################

    ## Count relations ########################################

    # Build a relation tuple
    def make_relation_tuple(series):
        kind = series['Type']
        master = series['Master ID']
        dependent = series['Dependent ID']

        #return (kind, master, dependent)
        return '%s||%s||%s' % (kind, master, dependent)

    # Get the relation counts
    def make_rel_dicts(frame):
        features = defaultdict(int)
        def inc(series):
            features[make_relation_tuple(series)] += 1
        frame.apply(inc, axis=1)
        return features

    for k in relations:
        relation_dicts[k] = make_rel_dicts(relations[k])
    ###########################################################

    # Add both dictionaries ###################################
    for k in entity_dicts:
        entity_dicts[k].update(relation_dicts[k])
    ###########################################################

    ## Make a sparse design matrix
    dv = DictVectorizer(sparse=False)
    X = dv.fit_transform([entity_dicts[k] for k in entity_dicts]).astype(np.int32)

    ## Do Affinity Propagation
    print "Doing affinity propagation"
    af = AffinityPropagation().fit(X)
    cluster_centers_indices = af.cluster_centers_indices_
    labels = pd.Series(af.labels_)

    # Binarize X
    X[X > 1] = 1


    ## Give an index to each document
    docs = {k:v for k, v in enumerate(entity_dicts.keys())}

    ## Sort X features by number of ocurrences
    sorted_columns = sorted(enumerate(X.sum(axis=0)), key=lambda x: x[1], reverse=True)
    ## Rearrange the matrix
    X = X[:, [s[0] for s in sorted_columns]]

    def bits2decimal(bits):
        ret = long(0)
        for i in xrange(bits.shape[0]-1, -1, -1):
            ret += bits[bits.shape[0]-1-i]*(long(2**i))
        return ret

    # Sort X documents by decimal value value
    sorted_rows = [x[0] for x in sorted(enumerate([bits2decimal(X[i, :]) for i in xrange(X.shape[0])]), key=lambda x: x[1], reverse=True)] #sort(X)
    X = X[sorted_rows, :]
    X = X[:, :129]

    plt.ion()
    fig, ax = plt.subplots()
    ax.set_yticks(np.arange(0,14)+0.5)
    ax.set_yticklabels([docs[i] for i in sorted_rows])
    ax.set_ylabel("Document")
    ax.set_xlabel("Feature number")
    ax.set_title("Feature heat map")
    plt.pcolor(X)
