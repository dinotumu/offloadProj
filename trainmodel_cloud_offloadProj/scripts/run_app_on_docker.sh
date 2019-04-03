#!/bin/sh

# # Arg 0 is PWD + '/scripts/run_app_on_docker.sh'
# echo "Arg 0: $0"
# # Arg 1 is PATH_TO_FILE_DIR 
# echo "Arg 1: $1"
# # Arg 2 is filename
# echo "Arg 2: $2"
# # Arg 3 is PATH_OCR_OUTPUT
# echo "Arg 3: $3"

# example output
# Arg 0: /home/dinotumu/Documents/offloadProj/trainmodel_cloud_offloadProj/scripts/run_app_on_docker.sh
# Arg 1: /home/dinotumu/Documents/offloadProj/trainmodel_cloud_offloadProj/data/test_images/
# Arg 2: 001.png
# Arg 3: /home/dinotumu/Documents/offloadProj/trainmodel_cloud_offloadProj/data/ocr_output/

# variables
FILE_PATH=$1
FILE_NAME=$2
OCR_OUTPUT_PATH=$3
FILE_PATH_NAME=$FILE_PATH$FILE_NAME
# echo "$FILE_PATH_NAME"
TMP=TMP_$$_$(date +"%N")

# run docker container
docker run -dt --name tesseract-cn tesseract

# # make temporary directory for sharing inout and output with host
# echo "docker exec -it tesseract-cn mkdir \-p ./$TMP/"
# echo "docker cp $FILE_PATH_NAME tesseract-cn:/home/app/$TMP/"


docker exec -it tesseract-cn mkdir \-p ./$TMP/
docker cp $FILE_PATH_NAME tesseract-cn:/home/app/$TMP/


# execute the tesseract command in the alpine linux shell
# echo "docker exec -it tesseract-cn /bin/ash -c \"cd ./$TMP/; tesseract ./$FILE_NAME $TMP\""
# echo "docker cp tesseract-cn:/home/app/$TMP/$TMP.txt ./data/output/"


docker exec -it tesseract-cn /bin/ash -c "cd ./$TMP/; tesseract ./$FILE_NAME $TMP.txt"
docker cp tesseract-cn:/home/app/$TMP/$TMP.txt $OCR_OUTPUT_PATH


# remove the temporary directory, stop and remove container instance
docker exec -it tesseract-cn rm \-r ./$TMP/
docker stop tesseract-cn
docker rm tesseract-cn