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
    
    output=$(python page_util.py $path)
    
    if [ "$LABEL" != "" ]; then
	echo "$output:$LABEL" > $WORDS_DIR/$name
    else
	echo "$output" > $WORDS_DIR/$name
    fi
done
