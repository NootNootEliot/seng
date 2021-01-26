#!/bin/bash
echo "Attempting decrypting data_pack.tar.gz.age"
age --decrypt -i ./private/key.txt ./data_pack.tar.gz.age > data_pack.tar.gz

echo "Making new data_pack folder"
mkdir data_pack

echo "Attempting decompression of data_pack.tar.gz into data_pack"
tar -xzf ./data_pack.tar.gz --directory ./data_pack

echo "Removing unneeded files"
rm -rf ./data_pack.tar.gz.age ./data_pack.tar.gz

echo "Finished"
