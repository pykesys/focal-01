#!/usr/bin/env bash

set -euo pipefail

export IMAGE_SEARCH_DATA_DIR="/tmp/image-search"
export IMAGE_SEARCH_IMAGE_DIR="${IMAGE_SEARCH_DATA_DIR}/image-dir"
export IMAGE_SEARCH_SQLITE_URL="sqlite:///${IMAGE_SEARCH_DATA_DIR}/image-search.sqlite"

mkdir -p ${IMAGE_SEARCH_IMAGE_DIR}

poetry run fastapi dev image_search/app.py
