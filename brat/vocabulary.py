''' Class that encapsulates a vocabulary for feature vectorizing '''

class Vocabulary:

    def __init__(self):
        self.encoded = {}
        self.decoded = {}
        self.ix = 0

    def encode(self, value, type):
        ''' Value is the feature val and type is the feature family. i.e. species, cell, ... '''

        key = '%s|%s' % (type, str(value))

        if key in self.encoded:
            return self.encoded[key]
        else:
            self.encoded[key] = self.ix
            self.decoded[self.ix] = key

            ret = self.ix
            self.ix += 1

        return ret

    def decode(self, ix):
        key = self.decoded[ix]

        # [type, value]
        return key.split('|', 1)

    @property
    def keys(self):
        return [self.decoded[i] for i in xrange(len(self))]

    def encode_fast(self, value, type):
        ''' Value is the feature val and type is the feature family. i.e. species, cell, ... '''

        key = '%s|%s' % (type, str(value))
        return self.encoded[key]

    def __len__(self):
        return len(self.encoded)
