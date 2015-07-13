''' Uses the gene/gene products dictionary to extract mentions of proteins (mostly) from the sentences '''

import sys, pickle

pdict = sys.argv[2]
pfile = sys.argv[1]

# Load the DICT
with open(pdict) as f:
	dict = pickle.load(f)

genes = [dict[k] for k in dict]


with open(pfile) as f:
	for line in f:
		line = line[:-1]
		num, _, __, text = line.split('\t')

		text = text.lower()
		for token in text.split():
			for gene in genes:
				mentions = []
				if token.startswith(gene):
					start = text.find(token)
					mentions.append((start, gene))

				if len(mentions) > 0:
					for m in mentions:
						print '%s\t%s\t%s' % (num, m[0], m[1])
