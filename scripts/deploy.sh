#!/bin/bash
# scripts/deploy.sh

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${YELLOW}Starting deployment...${NC}"

# Package Lambda functions
./scripts/package.sh

# Deploy infrastructure
cd terraform
terraform init
terraform plan -out=tfplan
terraform apply -auto-approve tfplan

if [ $? -eq 0 ]; then
    echo -e "${GREEN}Deployment successful!${NC}"
    
    # Get API Gateway URL
    API_URL=$(terraform output -raw api_url)
    echo -e "${GREEN}API URL: ${API_URL}${NC}"
else
    echo -e "${RED}Deployment failed!${NC}"
    exit 1
fi
