#!/bin/sh

# includes name as well
INPUT_DIR_NAME=$1
INPUT_NAME=$2

# output directory from arguments
OUTPUT_DIR=$3
OUTPUT_NAME=$4

# temporary directory
TMP=TMP_$$_$(date +"%N")

docker exec -t tesseract-cn mkdir -p ./$TMP/
docker cp $INPUT_DIR_NAME tesseract-cn:/home/app/$TMP/
docker exec -t tesseract-cn /bin/ash -c "cd ./$TMP/; tesseract $INPUT_NAME $OUTPUT_NAME"
docker cp tesseract-cn:/home/app/$TMP/$OUTPUT_NAME.txt $OUTPUT_DIR
docker exec -t tesseract-cn rm \-r ./$TMP/