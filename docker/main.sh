#!/bin/bash

# define constants
PWD=$(pwd)'/docker'
FILE_NAME='image.png'
FILE_PATH=$PWD'/data/input/'$FILE_NAME
OUTPUT_DIR=$PWD'/data/output/'
TMP=TMP_$$_$(date +"%N")

# start the 'tesseract-cn' container using the customised 'tesseract docker alpine linux' image
docker run -dt --name tesseract-cn tesseract

# make temporary directory for sharing input and output with host
docker exec -it tesseract-cn mkdir \-p ./$TMP/

# copy input image to docker shared storage volume
docker cp $FILE_PATH tesseract-cn:/home/app/$TMP/

# execute the tesseract command inside 'tesseract-cn' alpine linux shell
docker exec -it tesseract-cn /bin/ash -c "cd ./$TMP/; tesseract $FILE_NAME $FILE_NAME$TMP"

# get the output from the shared volume
docker cp tesseract-cn:/home/app/$TMP/$TMP.txt $OUTPUT_DIR

# remove all the temporary directories and files in the docker shared storage volume
docker exec -it tesseract-cn rm \-r ./$TMP/

# stop and remove docker container
docker stop tesseract-cn
docker rm tesseract-cn