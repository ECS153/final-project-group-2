#!/bin/bash

if [[ "$#" -ne 2 ]]; then
  echo "Incorrect number of parameters"
  echo "startNodes.sh <number of nodes in the mixnet> <hostname>"
  exit
fi

./genRSAKey.sh $1

for (( i = 0; i < $1; i++ )); do
  gnome-terminal -- python3 testMixNode.py $i $2
done

python3 ./server.py $2
