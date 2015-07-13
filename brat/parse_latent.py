''' Parses the brat annotation files to extract context labels '''
import sys
from utils import *

path = sys.argv[1]
errors = 0

tb, ev, rl = parse_standoff(path)

# Build the output string
for key in rl:
    try:
        kind, event, context = rl[key].split()

        if kind == 'ContextOf':
            id = event.split(':')[1][1:]
            context = tb[context.split(':')[1]]
            t = context.split()
            c_type, position, text = t[0], int(t[1]) ,' '.join(t[3:])

        # Print the context annotation
        print '%s:%i:%s:%s' % (id, position, c_type, text)
    except:
        errors += 1

#print "Errors: %i" % errors
