''' Builds a dictionary of ids for the context annotation species '''
import sys


operation = sys.argv[1].strip('-').lower()
pfile = sys.argv[2]

if operation == 'dict':
    with open(pfile) as f:
        dict = {}

        for l in f:
            l = l[:-1].lower()
            if l in ("mouse", 'mice') or 'mice' in l:
                dict[l] = 'ncbi-10088'
            elif l in ("human", "man", "men", "woman", "women", "person", "operator") or 'human' in l:
                dict[l] = "ncbi-9606"
            elif l in ("drosophila", 'fly') or 'drosophila' in l:
                dict[l] = 'ncbi-7215'
            elif l in ('murine','murinae') or 'murine' in l:
                dict[l] = 'ncbi-39107'
            elif l in ('xenopus', ) or 'xenopus' in l:
                dict[l] = 'ncbi-8353'


    for key in dict:
        print '%s\t%s' % (key, dict[key])

elif operation == 'ground':
    pdict = sys.argv[3]

    # Load the dictionary
    with open(pdict) as f:
        dict = {key:val for key, val in [l[:-1].split('\t') for l in f]}

    # Ground the context species annotation
    with open(pfile) as f:
        for line in f:
            nid, loc, kind, text = line[:-1].split(':')

            if kind == "Main-Species":
                text = dict[text.lower()]

            print '%s:%s:%s:%s' % (nid, loc, kind, text)
