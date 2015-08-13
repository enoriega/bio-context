''' This module will export a time series for every document based in the frames parsed in
    analytics.py '''

import os
import numpy as np
from analytics import *

def write_files(obs_matrices, latent_matrices, obs_voc, lat_voc, docs):
    ''' Writes the values to text files '''

    header_obs, header_lat = obs_voc, lat_voc

    header_obs = [h.replace(' ', '_') for h in header_obs]
    header_lat = [h.replace(' ', '_') for h in header_lat]

    if not os.path.exists('numbers'):
        os.makedirs('numbers')

    with open('numbers/directory.txt', 'w') as f, open('numbers/obs_labels.txt', 'w') as g,\
        open('numbers/states_labels.txt', 'w') as h:

        g.write('%s\n' % ' '.join(header_obs))
        h.write('%s\n' % ' '.join(header_lat))

        for i, d in enumerate(docs):
            pdir = 'p{0:02d}'.format(i+1)

            f.write('%s %s\n' % (pdir, d))
            pdir = os.path.join('numbers', pdir)

            if not os.path.exists(pdir):
                os.makedirs(pdir)

            m = obs_matrices[d]
            np.savetxt(os.path.join(pdir, 'obs.txt'), m, fmt='%i', delimiter=' ')
            m = latent_matrices[d]
            np.savetxt(os.path.join(pdir, 'states.txt'), m, fmt='%i', delimiter=' ')

obs_matrices, lat_matrices, lat_frames = {}, {}, {}

for doc in docs:
    # Generate a the observed feature matrix for the time series
    n_sentences = len(lines[doc]) # Number or sentences (lines) in the document
    obs = np.zeros((n_sentences, len(voc)), dtype=int) # The shape of the matrix is Sentence num x Size of the vocabulary
    latent = np.zeros((n_sentences, len(voc)), dtype=int)

    # Iterate through each line and activate the corresponding features
    for i in xrange(n_sentences):

        # Select the entities that appear in the
        ent = entities[doc]
        # Map the ids to their index in the row vector
        ix = ent[ent['Line Num'] == i]['Grounded ID'].map(lambda s: voc.get(s, -1))

        # Remove unresolved ids:
        ix = ix[ix != -1]

        # If there is an entity set it
        if len(ix) > 0:
            obs[i, ix] = 1
            latent[i, ix] = 1

        # Do the same for the relations
        rel = relations[doc]
        ix = rel[rel['Line Num'] == i].apply(lambda s: voc[make_relation_tuple(s)], axis=1)

        if len(ix) > 0:
            obs[i, ix] = 1
            latent[i, ix] = 1

    # Now remove the protein/gene/gene product elements from the latent state matrix
    # I use pandas to do this with few lines of code
    lat_frame = pd.DataFrame(latent).T # The column names are the id of the entities, transposed to make it the index
    lat_frame['id'] = voc

    # Remove the rows with uniprot and other ids
    lat_frame = lat_frame[(lat_frame.id.str.startswith('uniprot') == False) & (lat_frame.id.str.startswith('interpro') == False)]
    lat_voc = lat_frame.id.values
    del lat_frame['id']

    lat_frame = lat_frame.T

    # Retrieve the numpy matrix
    latent = lat_frame.values

    # Store
    obs_matrices[doc] = obs
    lat_matrices[doc] = latent
    lat_frames[doc] = lat_frame

# Write the files
write_files(obs_matrices, lat_matrices, voc, lat_voc, docs)
