#!/bin/bash
docker ps -f name=tesseract-cn
TMP=TMP_$$_$(date +"%N")
docker exec -it tesseract_container mkdir \-p ./$TMP/
docker cp ./input/image.jpg tesseract_container:/home/work/$TMP/
docker exec -it tesseract_container /bin/ash -c "cd ./$TMP/; tesseract ./image.jpg $TMP"
docker cp tesseract_container:/home/work/$TMP/$TMP.txt ./output/
docker exec -it tesseract_container rm \-r ./$TMP/
docker exec -it tesseract-cn ls