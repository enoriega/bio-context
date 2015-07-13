''' Heuristics to fill in context labels '''

import pandas as pd

def drag_context(m):
    ''' This just drags context till the end since it shows up '''

    m[m == 0] = np.nan
    df = pd.DataFrame(m)
    df.fillna(method='ffill', axis=0, inplace=True) # Propagare the context until the next appearance
    df.fillna(value=0., inplace=True)
    return df.values # Underlying array

def fill_context_events(m, d, context, events):
    c = context[context.doc == d][['event', 'line', 'type', 'text']].sort(['line']).drop_duplicates()

    # For each context annotation, we get the lines of all the events to which it belongs
    a = pd.merge(c, events[events.doc == d][['id', 'line']], how='left', left_on='event', right_on='id')

    for context_num in a.line_x.drop_duplicates():
        filtered_lines = a[a.line_x == context_num]
        e_lines = filtered_lines.line_y.drop_duplicates()

        # Extract the row of the matrix
        v = m[context_num, :]
        assert v.any(), "Line %i for doc %s should've context" % (context_num, d)

        for el in e_lines:
            # Propagate by addition
            start = min(context_num, el)
            end = max(context_num, el) + 1
            m[start:end, :] += v
        # Reestablish the binary property
        m[m > 1] = 1
        assert (m > 1).any() == False

    return m

def fill_between_events(m, d, context, events):

    c = context[context.doc == d][['event', 'line', 'type', 'text']].sort(['line']).drop_duplicates()

    # For each context annotation, we get the lines of all the events to which it belongs
    a = pd.merge(c, events[events.doc == d][['id', 'line']], how='left', left_on='event', right_on='id')

    for context_num in a.line_x.drop_duplicates():
        filtered_lines = a[a.line_x == context_num]
        fr, to = filtered_lines.line_y.min(), filtered_lines.line_y.max()

        # Extract the row of the matrix
        v = m[context_num, :]
        assert v.any(), "Line %i for doc %s should've context" % (context_num, d)
        # Propagate by addition
        m[fr:to+1] += v
        # Reestablish the binary property
        m[m > 1] = 1
        assert (m > 1).any() == False

    return m

def turn_on_context_mentions(m, d, lat_voc, species, genes, cells):
    ''' Turns on the context bit for named entity mentions '''

    sp = species[species.doc == d][['line', 'text']]
    gn = genes[genes.doc == d][['line', 'text']]
    cl = cells[cells.doc == d][['line', 'text']]

    for _, row in species.iterrows():
        ix, s = row.line, row.text
        m[ix, lat_voc.encode_fast(s, 'Main-Species')]

    return m
