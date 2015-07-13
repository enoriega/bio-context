''' Builds a dictionary of ids for the context annotation of cells '''
import sys
import pickle


operation = sys.argv[1].strip('-').lower()
pfile = sys.argv[2]

def normalize(name):
    ''' Heuristic to normalize cell type '''
    ret = name.lower()
    ret = ret.replace('cells', '')
    ret = ret.replace('cell', '')

    return ret.strip(' .,:;\n')

if operation == 'dict':
    pass # Now I have a manual dict

elif operation == 'ground':
    pdict = sys.argv[3]

    # Load the dictionary
    with open(pdict) as f:
        dict = pickle.load(f)

    # Make the dict a list
    cells = [dict[k] for k in dict]
    # Ground the context species annotation
    with open(pfile) as f:
        for line in f:
            nid, loc, kind, text = line[:-1].split(':')

            if kind in ("Cell-Type", "Cell-Line"):
                text = text.lower()
                for c in cells:
                    if c in text:
                        text = c
                        break
                #text = dict[text.lower()]

            print '%s:%s:%s:%s' % (nid, loc, kind, text)
