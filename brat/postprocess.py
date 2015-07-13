''' Post-process feature files to generate new features '''
import sys, os, codecs
from utils import *


fworkspace = sys.argv[1]
fcontext = sys.argv[2]
fevents = sys.argv[3]

# This is the prefix of the files for the given document
prefix = fcontext.split('/')[-1]
prefix = '.'.join(prefix.split('.')[:-1])

# Load the sentences offsets
sentences_spans = {}
sentences_text = {}
with codecs.open(os.path.join(fworkspace, prefix + '.sentences'), encoding='utf_8') as f:
    for line in f:
        ix, start, end, text = line.split('\t')
        sentences_spans[int(ix)] = (int(start), int(end))
        sentences_text[int(ix)] = text

# Load the context file contents
context = []
with open(fcontext) as f:
    for line in f:

        evid, position, kind, text = line[:-1].split(':')


        #TODO: Any postprocessing here
        position = get_sentence(position, sentences_spans)


        context.append((evid, position, kind, text))

# Write back the post-processed context labels
with open(fcontext, 'w') as f:
    for c in context:
        f.write('%s\n' % ':'.join(c))

# Load the events file contents
events = []
with open(fevents) as f:
    line = True #Ugly hack to bootstrap the loop
    while line:
        # Read the feature lines
        evid = int(f.readline())
        kind = f.readline()[:-1]
        position = int(f.readline())
        num_participants = int(f.readline())
        roles = f.readline()[:-1]
        pkinds = f.readline()[:-1]
        ptexts = f.readline()[:-1]

        participants = [(role, pkind, ptext) for role, pkind, ptext in
        zip(roles.split(), pkinds.split(), ptexts.split())]

        #TODO: Any postprocessing here
        position = get_sentence(position, sentences_spans)

        events.append([
            evid, kind, position, num_participants, participants
        ])

        # Necessary to consume the separating newline char
        line = f.readline()


# Write back the post-processed events labels
with open(fevents, 'w') as f:
    for i, e in enumerate(events):
        f.write('%i\n' % e[0]) # evid
        f.write('%s\n' % e[1]) # kind
        f.write('%s\n' % e[2]) # position
        f.write('%i\n' % e[3]) # num_participants

        for p in e[4]:
            f.write('%s\n' % p[0]) # role
            f.write('%s\n' % p[1]) # kind
            f.write('%s\n' % p[2]) # text

        if (i+1) != len(events):
            f.write('\n')
