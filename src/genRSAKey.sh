#!/bin/bash

if [[ "$#" -ne 1 ]]; then
  echo "Incorrect number of parameters"
  echo "Please enter ./genRSAKey.sh <number of keys to generate>"
  exit
fi

echo "Generating" $1 "key(s)..."


for (( i = 0; i < $1; i++ )); do
  echo "Generating Key #"$i
  openssl genrsa -out $i.pem 2048 > /dev/null 2>&1
  openssl rsa -in $i.pem -outform PEM -pubout -out $i.pub > /dev/null 2>&1
done

echo "Done."
