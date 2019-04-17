#!/bin/bash

# define constants
PWD=$(pwd)'/docker'
FILE_NAME='image.png'
FILE_PATH=$PWD'/data/input/'$FILE_NAME
OUTPUT_DIR=$PWD'/data/output/'
TMP=TMP_$$_$(date +"%N")

# start the 'tesseract-cn' container using the customised 'tesseract docker alpine linux' image
docker run -dt --name tesseract-cn tesseract

# copy input image to shared volume
docker exec -it tesseract-cn mkdir \-p ./$TMP/
docker cp $FILE_PATH tesseract-cn:/home/app/$TMP/

# execute the input using 'tesseract-cn' docker container
docker exec -it tesseract-cn /bin/ash -c "cd ./$TMP/; tesseract $FILE_NAME $TMP"

# get the output from the shared volume
docker cp tesseract-cn:/home/app/$TMP/$TMP.txt $OUTPUT_DIR
docker exec -it tesseract-cn rm \-r ./$TMP/

# stop and remove docker container
docker stop tesseract-cn
docker rm tesseract-cn