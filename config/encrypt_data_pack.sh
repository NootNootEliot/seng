#!/bin/bash
echo "Compressing data pack"
tar czf ./data_pack.tar.gz ./data_pack

echo "Getting public key"
public_key=$( cat private/public_key.txt )

echo "Encrypting compressed data pack"
age -o ./data_pack.tar.gz.age -r $public_key ./data_pack.tar.gz

echo "Removing all data_pack files but the encrypted one"
rm -rf ./data_pack ./data_pack.tar.gz

echo "Creation and encryption of data pack completed"
