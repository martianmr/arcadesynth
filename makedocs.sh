#!/bin/bash
rm -f docs/*.md
pydoc-markdown -m arcadesynth > docs/arcadesynth.md
for filename in src/arcadesynth/*.py
do
    modulename=$(basename $filename .py)
    if [ "$modulename" != "__init__" ]
    then
        pydoc-markdown -m arcadesynth.$modulename > docs/$modulename.md
    fi
done
