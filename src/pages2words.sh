#!/bin/sh
# Usage:
# ./pages2words.sh PAGE_DIR WORDS_DIR LABEL

PAGE_DIR=$1
WORDS_DIR=$2
LABEL=$3
paths=$(ls $PAGE_DIR/*)

for path in $paths; do
    name=$(basename $path)

    echo $path
    
    if [ "$LABEL" != "" ]; then
	echo $(python page_util.py $path)"\t$LABEL" #> $WORDS_DIR/$name 
    else
	echo $(python page_util.py $path) > $WORDS_DIR/$name 
    fi
done
