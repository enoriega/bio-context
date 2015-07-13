''' utils for parsing '''

def parse_standoff(path):
    tb = {}
    ev = {}
    rl = {}

    # Parse the file
    with open(path) as f:
        for line in f:
            key, val  = line[:-1].split('\t', 1)
            if key[0] == 'T':
                tb[key] = val
            elif key[0] == 'E':
                ev[key] = val
            elif key[0] == 'R':
                rl[key] = val

    return tb, ev, rl

def interval_contains(interval, item):
    if type(item) in (int, float):
        return True if item >= interval[0] and item <= interval[1] else False
    else:
        return True if item[0] >= interval[0] and item[1] <= interval[1] else False

def get_sentence(point, sentences):
    for key in sentences:
        if type(point) == str:
            point = int(point)

        if interval_contains(sentences[key], point):
            return str(key)
    raise KeyError()
