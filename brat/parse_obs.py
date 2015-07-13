''' Parses the brat annotation files to extract context labels '''
import sys
from utils import *

path = sys.argv[1]
errors = 0

tb, ev, rl = parse_standoff(path)

errors = 0

# Generate the features for each event
for i, key in enumerate(ev):
    try:
        id = key[1:]

        kind = ev[key].split(' ', 1)[0]
        participants = ev[key].split()[1:]

        kind, trigger = kind.split(':')

        # Position of the event within the paper
        absolute_position = tb[trigger].split()[1]

        # Participant features
        num_participants = len(participants)

        roles = []
        types = []
        names = []

        for participant in participants:
            # Role and name (to be normalized)
            role, ix = participant.split(':')

            if ix[0] == 'T':
                data = tb[ix].split()
            elif ix[0] == 'E':
                e = ev[ix]
                ix = e.split(' ')[0].split(':')[1] #Hack!
                data = tb[ix].split()

            roles.append(role)
            types.append(data[0])
            names.append(' '.join(data[3:]))

        assert len(roles) == len(types) == len(names), "Problem parsing the participants"

        print '%s' % id
        print '%s' % kind
        print '%s' % absolute_position
        print '%i' % num_participants
        print '%s' % '\t'.join(roles)
        print '%s' % '\t'.join(types)
        print '%s' % '\t'.join(names)

        if (i+1) != len(ev):
            print

    except Exception as e:
        errors += 1
