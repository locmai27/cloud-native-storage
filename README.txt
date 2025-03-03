CLOUD-NATIVE STORAGE

Cloud-Native Storage is a fully functional file storage solution that leverages AWS services and a modern web stack. It provisions AWS infrastructure with Terraform, provides a Flask-based backend API for file operations, and offers a React-based frontend for interacting with the service.

TABLE OF CONTENTS
1. Overview
2. Architecture
3. Requirements
4. Setup and Deployment
   - AWS Infrastructure Deployment
   - Backend Deployment
   - Frontend Deployment
5. Usage
6. Cleanup
7. Notes

1. OVERVIEW
This project provides a cloud-native solution for file storage where:
- Files are stored in an S3 bucket with server-side encryption.
- File metadata is saved in a DynamoDB table.
- AWS Lambda (running a Flask app) exposes API endpoints through API Gateway.
- CloudFront is configured to cache and serve files from the S3 bucket.
- A React frontend enables file upload, listing, download, and deletion.

2. ARCHITECTURE
- S3 Bucket: Stores uploaded files securely.
- DynamoDB Table: Holds metadata about each file.
- AWS Lambda: Runs the Flask backend that handles file operations.
- API Gateway: Provides HTTP endpoints to trigger the Lambda functions.
- CloudFront: Distributes files from S3 globally for fast access.
- React Frontend: Provides a user interface for interacting with the API.

3. REQUIREMENTS
- Terraform (v1.x or later)
- AWS CLI
- Python 3.9+
- Node.js and npm

4. SETUP AND DEPLOYMENT

   A. AWS INFRASTRUCTURE DEPLOYMENT
   1. Navigate to the "infrastructure" directory:
      cd infrastructure
   2. Initialize Terraform:
      terraform init
   3. Review the execution plan:
      terraform plan
   4. Apply the configuration:
      terraform apply
      Type "yes" when prompted. This will create your AWS resources (S3 bucket, DynamoDB table, IAM roles, Lambda, API Gateway, CloudFront, etc.).

   B. BACKEND DEPLOYMENT
   1. Navigate to the "backend" directory:
      cd backend
   2. Create and activate a Python virtual environment:
      - On macOS/Linux:
          python3 -m venv venv
          source venv/bin/activate
      - On Windows:
          python -m venv venv
          venv\Scripts\activate
   3. Install dependencies:
      pip install -r requirements.txt
   4. Package the application for AWS Lambda (if deploying to Lambda):
      - Run the packaging script:
        ./package_lambda.sh
      - Ensure the resulting deployment-package.zip is uploaded to your S3 bucket under the key "deployment-package.zip".
   5. Run the Flask backend locally:
      python3 app.py
      The application will run on http://127.0.0.1:5001

   C. FRONTEND DEPLOYMENT
   1. Navigate to the "frontend" directory:
      cd frontend
   2. Install Node.js dependencies:
      npm install
   3. Run the React development server:
      npm start
      The frontend will be available at http://localhost:3000

5. USAGE
- File Upload: Use the React frontend to select and upload files. The backend generates a pre-signed URL for direct S3 uploads.
- File Listing: The frontend displays a list of uploaded files by querying the backend, which reads metadata from DynamoDB.
- File Download & Deletion: Download and delete files using the respective API endpoints provided by the Flask app.

6. CLEANUP
To delete all AWS resources created by Terraform, run:
   terraform destroy
Confirm with "yes" when prompted. This will remove all AWS resources from your account.

7. NOTES
- Environment Variables: If environment variables (e.g., S3_BUCKET_NAME, DYNAMO_TABLE) are not set, the defaults defined in the code will be used.
- Production Considerations: For production deployments, update your Terraform configuration to use a remote backend for state management, and consider using a production-grade WSGI server for the Flask app.
- Reserved Environment Variables: AWS Lambda reserves certain environment variable names (e.g., AWS_REGION), so avoid using them in your configuration.
- .env Files: If you wish to load environment variables from a .env or .flaskenv file, install the python-dotenv package.

End of README
