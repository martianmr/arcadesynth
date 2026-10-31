#!/bin/bash
rm -f *.html
pydoc -w arcadesynth
for filename in ../src/arcadesynth/*.py
do
    modulename=$(basename $filename .py)
    if [ "$modulename" != "__init__" ]
    then
        pydoc -w arcadesynth.$modulename
    fi
done
source=$(dirname $(pwd))
target=https://github.com/martianmr/arcadesynth/blob/main
sed -i s#file:$source#$target# *.html
sed -i s#$source## *.html
