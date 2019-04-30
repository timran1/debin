#!/bin/sh

FILES=./binary/*
for f in $FILES
do
  echo "Processing $f file..."

  filename=$(basename $f)

  strip -g $f -o ./strip/$filename

  # take action on each file. $f store current file name
  #cat $f
done
