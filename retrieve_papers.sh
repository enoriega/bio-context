#!/bin/sh
# Retrieves the nxml files of a list of papers specified from the command line or
# the standard input
# ./retrieve_papers.sh PMC123456 PMC876556 ... PMC987657

URL='http://www.ncbi.nlm.nih.gov/pmc/oai/oai.cgi?verb=GetRecord&identifier=oai:pubmedcentral.nih.gov:%i&metadataPrefix=pmc'

function download {
  # This loop will download all the papers from the OAI-PMH Service
  for ARG in $@
  do
    echo "Downloading $ARG..."
    # Strip the PMC prefix
    ID=${ARG#PMC}
    # Download the article
    curl $(printf "$URL" $ID) -o $ARG.xml 2> /dev/null

    # Test whether the document was found
    grep "idDoesNotExist" $ARG.xml > /dev/null
    if [[ $? -ne 0 ]]
    then
      # Transform it into an NXML document
      xsltproc -o $ARG.nxml oaipmh2nxml.xsl $ARG.xml
    else
      echo "$ARG not found in the web service"
    fi

    # Delete the Metadata xml
    rm $ARG.xml
  done
}

# If there are arguments, use them as the PMC IDs, otherwise, read from the stdin
if [[ $# -gt 0 ]]
then
  download $@
else
  echo "Type the PMCIDs"
  while read ID
  do
    download $ID
  done
fi
