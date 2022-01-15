#!/bin/bash

# Version info
VERSION=1.0.0-beta

# Clear files
rm -r build dist package

# Build
pyinstaller src/gtit.py

# Create final folder and move files
mkdir package
tar -zcvf "package/gtit-$VERSION.tar" dist/gtit