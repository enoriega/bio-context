''' Uses CoreNLP to split sentences and generate a standoff file with sentences spans '''
import sys, os
from lxml import etree

# Outputdir
outputDir = sys.argv[1]

# File to process
path = sys.argv[2]

# Run CoreNLP
#os.system('java -mx3g -cp "../corenlp/*" edu.stanford.nlp.pipeline.StanfordCoreNLP -annotators tokenize,ssplit -file "%s" -outputDirectory "%s"' % (path, outputDir))

# Parse resulting XML
xml = os.path.join(outputDir, path.split(os.sep)[-1] + '.xml')
tree = etree.parse(xml)

# sentences
sentences = tree.xpath('//sentence')

for ix, s in enumerate(sentences):
    #ix = s.attrib['id']
    tokens = s.xpath('tokens/token')
    start = tokens[0].xpath('CharacterOffsetBegin')[0].text
    end = tokens[-1].xpath('CharacterOffsetEnd')[0].text
    text = ' '.join([t.xpath('word')[0].text for t in tokens]).encode('utf-8')#tokens[-1].xpath('Text')[0].text

    # Print the sentence id and span
    print "%s\t%s\t%s\t%s" % (ix, start, end, text)

# Remove the xml file
#os.remove(xml)
