#!/bin/bash
docker stop tesseract-cn
docker rm tesseract-cn
docker ps -f name=tesseract-cn