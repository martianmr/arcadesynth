#!/bin/bash
rm -f *.md
pydoc-markdown -m arcadesynth > arcadesynth.md
for filename in ../src/arcadesynth/*.py
do
    modulename=$(basename $filename .py)
    if [ "$modulename" != "__init__" ]
    then
        pydoc-markdown -m arcadesynth.$modulename > $modulename.md
    fi
done
