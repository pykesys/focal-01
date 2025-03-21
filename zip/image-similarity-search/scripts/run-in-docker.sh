#!/usr/bin/env bash

set -euo pipefail

docker build -t image-search .

IMAGE_SEARCH_DATA_DIR="/tmp/image-search-docker"
IMAGE_SEARCH_IMAGE_DIR="${IMAGE_SEARCH_DATA_DIR}/image-dir"
IMAGE_SEARCH_SQLITE_URL="sqlite:///${IMAGE_SEARCH_DATA_DIR}/image-search.sqlite"

mkdir -p ${IMAGE_SEARCH_IMAGE_DIR}

docker run --rm -it \
  -e IMAGE_SEARCH_IMAGE_DIR=${IMAGE_SEARCH_IMAGE_DIR} \
  -e IMAGE_SEARCH_SQLITE_URL=${IMAGE_SEARCH_SQLITE_URL} \
  -v /tmp:/tmp \
  -p 8000:8000 \
  image-search
