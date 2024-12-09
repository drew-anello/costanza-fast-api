#!/bin/bash

# Define the name of the zip file
ZIP_FILE="costanza_lambda.zip"

# Remove any existing zip file
rm -f $ZIP_FILE

(cd lib; zip ../$ZIP_FILE -r .)

cd .. 
# Zip the FastAPI project files
zip -u $ZIP_FILE main.py models.py database.py requirements.txt Dockerfile

# Print a message indicating the zip file has been created
echo "Created $ZIP_FILE for deployment."