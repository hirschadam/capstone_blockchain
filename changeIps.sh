#!/bin/bash

newIp="$(ip a | grep 129.21..*/ -o | sed 's/\///')"
oldIp="$(cat node1.txt | grep 129.21..*$ -o)"

sed -ie "s/$oldIp/$newIp/g" *.txt
rm *.txte
