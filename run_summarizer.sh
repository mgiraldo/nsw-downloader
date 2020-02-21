#!/bin/bash
: '
  Assumes:
  - a summarizer server running at: http://localhost:4567/ via Docker for Mac
  - an image server running at: http://host.docker.internal:8000/ 
    (the way Docker for Mac does same host networking)
  - the existence of a image list in ../data/files-urls.csv
  - the existence of an output folder in ../data/colors_output
'
COUNT=0
STARTTIME=$(date +%s)
while IFS=, read -r file_key master_pid access_pid
do
  if [ $file_key != file_key ]
  then
    python summarizer.py -w ${file_key//\"/} ../data/colors_output/${access_pid//\"/}.json
  fi
  let COUNT=COUNT+1
done < ../data/files-urls.csv
ENDTIME=$(date +%s)
echo "Processed ${COUNT} files in $(($ENDTIME - $STARTTIME)) seconds."