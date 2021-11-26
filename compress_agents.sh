#!/bin/bash

find . -name "*.log" -delete
find . -name "*.tar.gz" -delete

for d in */ ; do
  dir_name=`basename "${d}"`
  tar cf "${dir_name}".tar.gz "${dir_name}"
done
