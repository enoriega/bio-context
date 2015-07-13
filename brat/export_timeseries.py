''' Generates time series latent and observed state for the HMMesque models '''
import pandas as pd
from analytics import *
from vocabulary import Vocabulary
from fillin_heuristics import *

### Build vocabularies
obs_voc = Vocabulary()

for val in species.text.drop_duplicates():
    obs_voc.encode(val, 'species')

for val in cells.text.drop_duplicates():
    obs_voc.encode(val, 'cells')

for val in genes.text.drop_duplicates():
    obs_voc.encode(val, 'genes')

for val in relations[['first', 'second', 'type']].drop_duplicates().iterrows():
    t = val[1]
    val = '%s|%s|%s' % (t[0], t[1], t[2])
    obs_voc.encode(val, 'relations')


lat_voc = Vocabulary()

for ix, t in context[['type', 'text']].drop_duplicates().iterrows():
    kind, val = t
    lat_voc.encode(val, kind)
#####################

## Build feature matrices
obs_matrices = {}
for d in documents:

    s = species[species.doc == d][['line', 'text']]
    c = cells[cells.doc == d][['line', 'text']]
    g = genes[genes.doc == d][['line', 'text']]
    r = relations[relations.doc == d][['line', 'first', 'second', 'type']]
    #con = context

    shape = (lines[lines.doc == d].shape[0], len(obs_voc))
    m = np.zeros(shape)

    for i in xrange(shape[0]):
        # Species
        for val in s[s.line == i].text:
            j = obs_voc.encode(val, 'species')
            m[i, j] = 1
            pass

        # Cells
        for val in c[c.line == i].text:
            j = obs_voc.encode(val, 'cells')
            m[i, j] = 1
            pass

        # Gene products
        for val in g[g.line == i].text:
            j = obs_voc.encode(val, 'genes')
            m[i, j] = 1
            pass

        # Relations
        for val in r[r.line == i][['first', 'second', 'type']].iterrows():
            t = val[1]
            val = '%s|%s|%s' % (t[0], t[1], t[2])
            j = obs_voc.encode(val, 'relations')
            m[i, j] = 1
            pass

    obs_matrices[d] = m.astype(np.int)


########################

# Build latent state matrices
latent_matrices = {}

for d in documents:
    shape = (lines[lines.doc == d].shape[0], len(lat_voc))
    m = np.zeros(shape)

    c = (context[context.doc == d][['line', 'text', 'type']]).drop_duplicates()
    c.set_index('line', inplace=True)

    for i in xrange(shape[0]):
        try:
            slice = c.loc[i, ['text', 'type']]
            rows = slice.values

            if len(rows.shape) == 1:
                rows = [rows]

            for row in rows:
                val, kind = row
                j = lat_voc.encode_fast(val, kind)
                m[i, j] = 1
        except KeyError as e:
            pass

    # Fill in context between the context annotation and the events

    fill_context_events(m, d, context, events)


    # Perform propagation heuristic
    #m = drag_context(m)
    ###############################

    # Fill between events heuristic
    fill_between_events(m, d, context, events)
    ###############################

    # Fill context for mentions
    turn_on_context_mentions(m, d, lat_voc, species, genes, cells)

    latent_matrices[d] = m.astype(np.int)
######################################

def write_files():
    ''' Writes the values to text files '''

    header_obs, header_lat = obs_voc.keys, lat_voc.keys

    header_obs = [h.replace(' ', '_') for h in header_obs]
    header_lat = [h.replace(' ', '_') for h in header_lat]

    with open('numbers/directory.txt', 'w') as f, open('numbers/obs_labels.txt', 'w') as g,\
        open('numbers/states_labels.txt', 'w') as h:

        g.write('%s\n' % ' '.join(header_obs))
        h.write('%s\n' % ' '.join(header_lat))

        for i, d in enumerate(documents):
            pdir = 'p{0:02d}'.format(i+1)

            f.write('%s %s\n' % (pdir, d))
            pdir = os.path.join('numbers', pdir)

            if not os.path.exists(pdir):
                os.makedirs(pdir)

            m = obs_matrices[d]
            np.savetxt(os.path.join(pdir, 'obs.txt'), m, fmt='%i', delimiter=' ')
            m = latent_matrices[d]
            np.savetxt(os.path.join(pdir, 'states.txt'), m, fmt='%i', delimiter=' ')
