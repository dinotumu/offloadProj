#!/bin/sh

# # Arg 0 is PWD + '/scripts/run_app_on_docker.sh'
# echo "Arg 0: $0"
# # Arg 1 is filename
# echo "Arg 1: $1"

# variables
PWD='/home/dinotumu/Documents/offloadProj/trainmodel_cloud_offloadProj'
FILE_NAME='001.png'
FILE_PATH=$PWD'/data/input/'$FILE_NAME
OUTPUT_DIR=$PWD'/data/output/'
TMP=TMP_$$_$(date +"%N")

# run docker container
docker run -dt --name tesseract-cn tesseract

# make temporary directory for sharing input and output with host
docker exec -it tesseract-cn mkdir \-p ./$TMP/
docker cp $FILE_PATH tesseract-cn:/home/app/$TMP/

# execute the tesseract command in the alpine linux shell
docker exec -it tesseract-cn /bin/ash -c "cd ./$TMP/; tesseract $FILE_NAME $FILE_NAME$TMP"
docker cp tesseract-cn:/home/app/$TMP/$FILE_NAME$TMP.txt $OUTPUT_DIR

# remove the temporary directory, stop and remove container instance
docker exec -it tesseract-cn rm \-r ./$TMP/
docker stop tesseract-cn
docker rm tesseract-cn