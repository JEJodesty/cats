#!/bin/bash

# Define the prefix
prefix="your_prefix"

# Generate a unique hash (using date and random number for uniqueness)
unique_hash=$(date +%s%N | sha256sum | head -c 8)

# Create the directory name by combining the prefix and unique hash
dir_name="${prefix}_${unique_hash}"

# Create the subdirectory
mkdir "$dir_name"

ipfs get {input_dir_cid} -o "$DIR_NAME"

# Output the directory name
echo "Created directory: $dir_name"
