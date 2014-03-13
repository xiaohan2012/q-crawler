#!/bin/sh

PAGE_DIR=$1
WORDS_DIR=$2

paths=$(ls $PAGE_DIR/*)

for path in $paths; do
    name=$(basename $path)
    echo "python page_util.py $path > $WORDS_DIR/$name"
done
