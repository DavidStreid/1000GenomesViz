#!/bin/bash
host="http://search-genomic-visualization-en4vqbwhnt5h7cx576wkaqweim.us-west-2.es.amazonaws.com/_bulk"
curl="curl -s -XPOST "
optns=" -H 'Content-Type:application/json' --data-binary "
fileExt="_mutFreq.json"
echo="; echo"

for f in *.json
do
	pop=(${f//_/ })
	url=$host$pop
	eval $curl$host$optns'"@'$pop$fileExt'"'$echo	
done
