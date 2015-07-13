#!/bin/sh
# Downloads external dependencies to initialize the workspace

# Download Linnaeus and the dictionary
echo "Downloading Linnaeus"
curl "http://iweb.dl.sourceforge.net/project/linnaeus/Linnaeus/linnaeus-2.0.tar.gz" -o "linnaeus-2.0.tar.gz"
tar -xzf "linnaeus-2.0.tar.gz"
mv linnaeus/bin/linnaeus-2.0.jar .
rm -rf linnaeus/ linnaeus-2.0.tar.gz

curl "http://iweb.dl.sourceforge.net/project/linnaeus/Entity_packs/species-proxy-1.2.tar.gz" -o "species.tar.gz"
tar xzf species.tar.gz
rm species.tar.gz

# Download CoreNLP
echo "Downloading CoreNLP"
curl "http://nlp.stanford.edu/software/stanford-corenlp-full-2015-04-20.zip" -o "corenlp.zip"
unzip corenlp.zip
mv stanford-corenlp-full-2015-04-20 corenlp
rm corenlp.zip

echo "Done!!"
