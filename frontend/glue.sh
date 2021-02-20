#!/bin/sh
while true
do
  aws s3 sync ~/Downloads s3://album-1/ --exclude "*" --include "*.flv"
  sleep 15
done