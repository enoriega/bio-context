''' Maps brat annotated soff file annotations to odin sentences '''

import glob
import pandas as pd
from collections import defaultdict
import os
import itertools as it

def mkETuple(line):
    tokens = line.split()
    return [tokens[0]] + [t.split(':')[1] for t in tokens[1:]]

def mkTTuple(line):
    tokens = line.split()
    return tokens[0], (int(tokens[2]), int(tokens[3]))

def make_span(event, tb):
    spans = [tb[e] for e in event[1:] if e[0] == 'T']
    return (min([s[0] for s in spans]), max([s[1] for s in spans]))

def resolve_line(text, lines, last):
    tokenized = text.replace(',', ' ,').replace('(', '( ').replace(')', ' )').replace('/', ' and ')

    if '.' in tokenized:
        if tokenized.index('.') < (len(tokenized)/2):
            tokenized = ''.join(it.dropwhile(lambda c: c != '.', tokenized)).strip('. ')
        else:
            tokenized = ''.join(it.takewhile(lambda c: c != '.', tokenized)).strip(' .')

    ls = []

    for (i, row) in lines.iterrows():

        if row['Line Num'] < last:
            continue

        if tokenized in row['Text']:
            ls.append(row['Line Num'])

    if len(ls) > 0:
        return pd.Series(ls)
    else:
        return None



output = defaultdict(list)
prefixes={s.split('/')[-1].split('.')[0] for s in glob.iglob('brat_sof/*')}
k, q, m, n, o = 0, 0, 0 , 0, 0

for p in prefixes:
    last = 0
    soff, text, pdlines = 'brat_sof/'+ p+'.ann', 'brat_sof/'+p+'.txt', pd.read_csv('tsv/'+p+'.lines', sep='\t')

    with open(soff) as f:
        lines = f.readlines()
        lines = [l.replace('\n', ' ') for l in lines]

    with open(text) as f:
        text = f.read()
        text = text.replace('\n', ' ')

    cix = [(c.split()[-2].split(':')[-1], c.split()[-1].split(':')[-1]) for c in [l for l in lines if 'ContextOf' in l]]
    cix = map(lambda x: (x[1], x[0]) if x[0][0] == 'T' and x[1][0] == 'E' else x, cix)

    events = [mkETuple(e) for e in lines if e[0] == 'E']
    # Filter events only to those that have context
    ev = {x[0] for x in cix}
    events = filter(lambda e: e[0] in ev, events)

    tb = {k:v for k, v in [mkTTuple(t) for t in lines if t[0] == 'T']}

    events = map(lambda x: (x[0], make_span(x, tb)), events)
    valid = {c[1] for c in cix}
    textbound = {k:tb[k] for k in filter(lambda k: k in valid, tb)}

    #sort events by location of their trigger
    events = {e[0]:e for e in events}

    cix = sorted(cix, key=lambda x:events[x[0]][1][0])

    # Resolve context sentences

    #Resolve event sentences

    # cache = {}
    # print "Now working on: %s" % p
    # for e, c in cix:
    #     try:
    #         e = events[e]
    #         nums = resolve_line(text[e[1][0]-2:e[1][1]+2], pdlines, last)
    #         if nums is None or nums.shape[0] == 0:
    #             if e[0] in cache:
    #                 num = cache[e[0]]
    #                 output[p].append((e[0], num, text[e[1][0]:e[1][1]], c))
    #             else:
    #                 k += 1
    #                 chunk = text[e[1][0]-15:e[1][1]+15].replace('\n', '')
    #                 print "%s\tNo match for:" % p
    #                 print chunk
    #                 os.system('echo "%s" | pbcopy' % chunk)
    #                 num = int(raw_input('>'))
    #                 print
    #                 output[p].append((e[0], num, text[e[1][0]:e[1][1]], c))
    #                 cache[e[0]] = num
    #         elif nums.shape[0] == 1:
    #             q += 1
    #             output[p].append((e[0], nums.iloc[0], text[e[1][0]:e[1][1]], c))
    #             last = nums.iloc[0]
    #         else:
    #             m += 1
    #             print 'Select a line number for:\n%s\n' % text[e[1][0]-15:e[1][1]+15]
    #             for n in nums:
    #                 print '%i:\t%s' % (n, pdlines.loc[n, 'Text'])
    #
    #             num = int(raw_input('>'))
    #             print
    #             output[p].append((e[0], num, text[e[1][0]:e[1][1]], c))
    #
    #     except Exception as a:
    #         n += 1
    #         output[p].append((e[0], -2, text[e[1][0]:e[1][1]], c))
    #         print a, type(a)
    #
    #     o += 1

    print "Now working on: %s" % p
    for element in backup[p]:
        if element[1] == -1:
            key = element[0]
            try:
                e = textbound[key]
                nums = resolve_line(text[e[0]-2:e[1]+2], pdlines, last)
                if nums is None or nums.shape[0] == 0:
                    k += 1
                    chunk = text[e[0]-10:e[1]+10].replace('\n', '')
                    print "%s\tNo match for:" % p
                    print chunk
                    os.system('echo "%s" | pbcopy' % chunk)
                    num = int(raw_input('>'))
                    print
                    output[p].append((key, num, text[e[0]:e[1]], c))
                elif nums.shape[0] == 1:
                    q += 1
                    output[p].append((key, nums.iloc[0], text[e[0]:e[1]], c))
                    last = nums.iloc[0]
                else:
                    m += 1
                    chunk = text[e[0]-15:e[1]+15].replace('\n', '')
                    print 'Select a line number for:\n%s\n' % chunk
                    for n in nums:
                        print '%i:\t%s' % (n, pdlines.loc[n, 'Text'])

                    os.system('echo "%s" | pbcopy' % chunk)
                    num = int(raw_input('>'))
                    print
                    output[p].append((key, num, text[e[0]:e[1]], c))

            except Exception as a:
                n += 1
                output[p].append((key, -2, text[e[0]:e[1]], c))
                print a, type(a)

        o += 1

print k, q, m, n, o
