#!/bin/bash

# Define the name of the zip file
ZIP_FILE="costanza_lambda.zip"

# Remove any existing zip file
rm -f $ZIP_FILE

# Zip the FastAPI project files
zip -r $ZIP_FILE main.py models.py database.py requirements.txt

# Print a message indicating the zip file has been created
echo "Created $ZIP_FILE for deployment."