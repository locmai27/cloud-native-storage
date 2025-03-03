#!/bin/bash
set -e

# Variables
BACKEND_DIR="backend"
PACKAGE_NAME="deployment-package.zip"
TEMP_DIR="package"

# Clean up any previous builds
echo "Cleaning previous package directory and zip file..."
rm -rf "$TEMP_DIR" "$PACKAGE_NAME"

# Create a temporary directory for packaging
mkdir -p "$TEMP_DIR"

# Install dependencies into the temporary directory (if requirements.txt exists)
if [ -f "$BACKEND_DIR/requirements.txt" ]; then
    echo "Installing Python dependencies..."
    pip install -r "$BACKEND_DIR/requirements.txt" -t "$TEMP_DIR"
fi

# Copy your backend source code into the package directory
echo "Copying source files from $BACKEND_DIR..."
cp -r "$BACKEND_DIR"/* "$TEMP_DIR/"

# Create the zip package from the temporary directory
echo "Creating deployment package $PACKAGE_NAME..."
cd "$TEMP_DIR"
zip -r "../$PACKAGE_NAME" . > /dev/null
cd ..

echo "Package created: $PACKAGE_NAME"
