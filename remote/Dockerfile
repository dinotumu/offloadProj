#
# Alpine Linux - Tesseract OCR - Docker Container
# Installs most recent version available from the main repository using Alpine Package Manager
# Link for the Tesseract OCR main repository: https://github.com/tesseract-ocr/tesseract/releases
# Link for Alpine Linux Tesseract OCR package: https://pkgs.alpinelinux.org/package/edge/community/x86/tesseract-ocr
#

FROM alpine:3.9

RUN apk update \
&& apk add --no-cache wget \
&& apk add --no-cache --update tesseract-ocr

RUN mkdir /home/app
WORKDIR /home/app