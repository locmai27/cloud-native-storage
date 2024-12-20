#!/bin/bash
# scripts/package.sh

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check if the script is run from the root directory
if [ ! -f "requirements.txt" ]; then
    echo -e "${YELLOW}Please run this script from the root directory of the project.${NC}"
    exit 1
fi

echo -e "${YELLOW}Packaging Lambda functions...${NC}"

# Create temporary directory for packaging
mkdir -p build

# Create virtual environment for dependencies
python3 -m venv build/venv
source build/venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create Lambda layer
cd ./build/venv/lib/python3.12/site-packages
zip -r ../../../../lambda_layer.zip .
cd ../../../../../


# Package Lambda functions
zip -r upload_function.zip ./src/functions/upload/
zip -r lib.zip ./src/lib/
zip -r models.zip ./src/models/

echo -e "${GREEN}Packaging complete!${NC}"

