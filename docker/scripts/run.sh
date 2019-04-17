#!/bin/bash
docker run -dt --name tesseract_cn tesseract
docker ps -f name=tesseract_cn