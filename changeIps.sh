#!/bin/bash

newIp="$(ifconfig | grep 129.21..*Bc -o | sed 's/Bc//')"
oldIp="$(cat nodes/node1.txt | grep 129.21..*$ -o)"

cd nodes
sed -i "s/$oldIp/$newIp/g" *.txt
rm *.txte 2>/dev/null
cd ../peers
sed -i "s/$oldIp/$newIp/g" *.txt
rm *.txte 2>/dev/null
