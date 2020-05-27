#!/bin/bash

if [[ "$#" -ne 2 ]]; then
  echo "Incorrect number of parameters"
  echo "startNodes.sh <number of nodes in the mixnet> <hostname>"
  exit
fi

./genRSAKey.sh $1

for (( i = 0; i < $1; i++ )); do
  echo "Creating node#" $i
  osascript -e 'tell application "Terminal" to activate' \
    -e 'tell application "System Events" to keystroke "t" using {command down}' \
    -e "tell application \"Terminal\" to do script \"python3.6 node.py '$i' '$2' '$1'\" in front window"
done

python3.6 ./server.py $2 $1
