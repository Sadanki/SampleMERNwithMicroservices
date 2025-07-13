#!/bin/bash
set -e

IMAGE_NAME=$1

echo "[*] Building Docker image: $IMAGE_NAME"
docker build -t $IMAGE_NAME .
