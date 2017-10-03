#!/bin/bash

# This script converts multi-page outlines to jpg files. 
# It makes a directory in the directory this script is invoked on.


CUR_DIR=`pwd`
PDF_FILE_PATH="$CUR_DIR/$1"
NEW_DIR="$CUR_DIR/outline_jpgs_tiffs_txts"

mkdir "$NEW_DIR"

pushd "$NEW_DIR"
  echo "Converting PDFS to PPMs..."
  pdftoppm "$PDF_FILE_PATH" outline_jpg
  echo "Converting PPMs to JPGS..."
  for i in `ls *.ppm`; do
    convert "$i" "$i.jpg"
  done
  echo "Removing PPMs..."
  rm -rf *.ppm
  mkdir "outline_tiffs"
  mkdir "outline_txts"
  echo "Working the magic now..."
  for i in `ls -A *.jpg`; do
    # http://www.fmwconcepts.com/imagemagick/textcleaner/index.php
    name=$(echo "$i" | cut -d"." -f1,3)
    ~/textcleaner.sh -g -e stretch -f 25 -o 20 -t 30 -u -s 1 -T -p 20 $i $name || exit
    rm $i
    # Tiff images are used by tesseract for optical character recognition
    convert $name "outline_tiffs/$name.tiff"

    # Using tesseract to convert to text file
    echo "Processing $name ..."
    tesseract "outline_tiffs/$name.tiff" "outline_txts/$(echo $name | cut -d"." -f1)" -psm 6
  done
popd

