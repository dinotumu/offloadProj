#!/bin/bash
docker run -dt --name tesseract-cn tesseract
TMP=TMP_$$_$(date +"%N")
docker exec -it tesseract-cn mkdir \-p ./$TMP/
docker cp ./input/image.jpg tesseract-cn:/home/work/$TMP/
docker exec -it tesseract-cn /bin/ash -c "cd ./$TMP/; tesseract ./image.jpg $TMP"
docker cp tesseract-cn:/home/work/$TMP/$TMP.txt ./output/
docker exec -it tesseract-cn rm \-r ./$TMP/
docker stop tesseract-cn
docker rm tesseract-cn