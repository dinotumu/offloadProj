#!/bin/sh

PWD='/home/dinotumu/Documents/offloadProj/cloud_offloadProj'
FILE_NAME='image.png'
FILE_PATH=$PWD'/data/input/'$FILE_NAME
OUTPUT_DIR=$PWD'/data/output/'
TMP=TMP_$$_$(date +"%N")


docker run -dt --name tesseract-cn tesseract
docker exec -it tesseract-cn mkdir \-p ./$TMP/
docker cp $FILE_PATH tesseract-cn:/home/app/$TMP/
docker exec -it tesseract-cn /bin/ash -c "cd ./$TMP/; tesseract $FILE_NAME $TMP"
docker cp tesseract-cn:/home/app/$TMP/$TMP.txt $OUTPUT_DIR
docker exec -it tesseract-cn rm \-r ./$TMP/
docker stop tesseract-cn
docker rm tesseract-cn