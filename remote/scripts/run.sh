#!/bin/sh

PWD='/home/dinotumu/Documents/offloadProj/train'
FILE_NAME=$1
FILE_PATH=$PWD'/data/train_data/'$FILE_NAME
# echo $FILE_PATH
OUTPUT_DIR=$PWD'/data/ocr_output/'
TMP=TMP_$$_$(date +"%N")


# docker run -dt --cpus="4.0" --name tesseract-cn tesseract
docker exec -it tesseract-cn mkdir -p ./$TMP/
docker cp $FILE_PATH tesseract-cn:/home/app/$TMP/
docker exec -it tesseract-cn /bin/ash -c "cd ./$TMP/; tesseract $FILE_NAME $TMP"
docker cp tesseract-cn:/home/app/$TMP/$TMP.txt $OUTPUT_DIR
docker exec -it tesseract-cn rm \-r ./$TMP/
# docker stop tesseract-cn
# docker rm tesseract-cn