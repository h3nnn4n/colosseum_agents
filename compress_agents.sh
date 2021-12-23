#!/bin/bash

find . -name "*.log" -delete
find . -name "*.tar.gz" -delete

for game_dir in */ ; do
  cd "${game_dir}"

  for agent_dir in */ ; do
    dir_name=`basename "${agent_dir}"`
    tar cf "${dir_name}".tar.gz "${dir_name}"
  done

  cd ..
done
