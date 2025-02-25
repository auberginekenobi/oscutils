#!/bin/bash

## Create a genes x samples expression table from a set of .genes.results files from RSEM.
## Usage: paste-rsem.sh DIRECTORY_CONTAINING_RSEM_RESULTS OUTFILE

INPUTDIR=$1
OUTFILE=$2

first=true
for file in $INPUTDIR/*.genes.results; do
	SAMPLE=$(basename $file .genes.results)
	echo "Writing $SAMPLE ..."
	if [ $first = true ]; then
		awk -v header=$SAMPLE 'BEGIN {OFS="\t"} NR==1 {print $1, header} NR>1 {print $1, $5}' "$file" > $OUTFILE
		first=false
	else
		paste "$OUTFILE" <(awk -v header=$SAMPLE 'BEGIN {OFS="\t"} NR==1 {print header} NR>1 {print $5}' $file) > temp.txt && \
		mv temp.txt $OUTFILE
	fi
done
echo "Done. RSEM results aggregated to $OUTFILE."
