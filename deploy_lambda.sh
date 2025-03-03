#!/bin/bash
set -e

# Variables
BACKEND_DIR="backend"
PACKAGE_NAME="deployment-package.zip"
TEMP_DIR="package"

# Clean up previous build
rm -rf "$TEMP_DIR" "$PACKAGE_NAME"

# Create a temporary directory
mkdir -p "$TEMP_DIR"

# Install dependencies locally into the package folder (if requirements.txt exists)
if [ -f "$BACKEND_DIR/requirements.txt" ]; then
    pip install -r "$BACKEND_DIR/requirements.txt" -t "$TEMP_DIR"
fi

# Copy your application code into the package directory
cp -r "$BACKEND_DIR"/* "$TEMP_DIR/"

# Create a ZIP file from the package directory
cd "$TEMP_DIR"
zip -r "../$PACKAGE_NAME" .
cd ..

echo "Deployment package created: $PACKAGE_NAME"
