#!/bin/bash
set -e

IMAGE_NAME=$1
AWS_ACCOUNT_ID=975050024946
REGION=ap-south-1
REPO_NAME=$IMAGE_NAME

echo "[*] Logging in to Amazon ECR"
aws ecr get-login-password --region $REGION | \
docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com

echo "[*] Tagging and pushing image to ECR"
docker tag $IMAGE_NAME:latest $AWS_ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$REPO_NAME:latest
docker push $AWS_ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$REPO_NAME:latest
