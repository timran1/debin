#!/bin/bash

CUR_DIR=$(pwd)

FILES=${CUR_DIR}/binary-orig/*
for f in $FILES
do
  echo "Processing $f file..."

  filename=$(basename $f)

  # strip -g $f -o ./strip/$filename
  which pushd
  pushd /store/multiverse/multiverse

  ./multiverse.py --execonly --arch x86-64 $f

  popd

  mv $f-r ./binary/$filename

  echo
  echo
  # take action on each file. $f store current file name
  #cat $f
done
