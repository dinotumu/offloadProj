#!/bin/sh
docker run -dt --name tesseract-cn tesseract
TMP=TMP_$$_$(date +"%N")
docker exec -it tesseract-cn mkdir \-p ./$TMP/
docker cp ./data/input/image.png tesseract-cn:/home/app/$TMP/
docker exec -it tesseract-cn /bin/ash -c "cd ./$TMP/; tesseract ./image.png $TMP"
docker cp tesseract-cn:/home/app/$TMP/$TMP.txt ./data/output/
docker exec -it tesseract-cn rm \-r ./$TMP/
docker stop tesseract-cn
docker rm tesseract-cn