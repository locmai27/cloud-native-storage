import os, uuid, time
from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
import boto3
from botocore.exceptions import ClientError
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

# Configuration 
AWS_REGION     = os.getenv('AWS_REGION', 'us-east-1')
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME', 'filestore-uploads-bucket')
DYNAMO_TABLE = os.getenv('DYNAMO_TABLE', 'filestore-FileMetadata')
# (If using AWS credentials via environment for local dev; on AWS Lambda/EC2, use IAM roles)
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')


# Initialize AWS clients/resources
if AWS_ACCESS_KEY:
    s3_client = boto3.client('s3', region_name=AWS_REGION,
                             aws_access_key_id=AWS_ACCESS_KEY,
                             aws_secret_access_key=AWS_SECRET_KEY)
    dynamo = boto3.resource('dynamodb', region_name=AWS_REGION,
                             aws_access_key_id=AWS_ACCESS_KEY,
                             aws_secret_access_key=AWS_SECRET_KEY)
else:
    # If no explicit creds, will use IAM role creds (e.g., on AWS Lambda/EC2)
    s3_client = boto3.client('s3', region_name=AWS_REGION)
    dynamo    = boto3.resource('dynamodb', region_name=AWS_REGION)

metadata_table = dynamo.Table(DYNAMO_TABLE)

# (Optional) Authentication via JWT (e.g., AWS Cognito JWT verification)
import functools, jwt
# Assume if using Cognito, we have a Cognito JWKS or a JWT secret for custom JWT
COGNITO_POOL_ID = os.getenv('COGNITO_POOL_ID')
JWT_SECRET = os.getenv('JWT_SECRET')  # if using custom JWTs

def token_required(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        token = None
        # JWT expected in Authorization header as "Bearer <token>"
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split("Bearer ")[1]
        if token is None:
            return jsonify({"error": "Authorization token required"}), 401
        try:
            # If using Cognito, verify using Cognito's public keys (not shown for brevity)
            # If using a custom JWT, decode with secret:
            decoded = jwt.decode(token, JWT_SECRET, algorithms=["HS256"]) if JWT_SECRET else {}
            # (In practice, verify audience, issuer, expiration, etc.)
        except Exception as e:
            return jsonify({"error": "Invalid token: %s" % str(e)}), 401
        # Optionally, set user info from decoded token (not used in this simple example)
        return f(*args, **kwargs)
    return wrapper

# Endpoint: Generate a pre-signed URL for uploading a file
@app.route('/files/presign', methods=['POST'])
#@token_required  # (optional, require auth to get upload URL)
def get_presigned_url():
    data = request.get_json()
    filename = data.get('filename')
    if not filename:
        return jsonify({"error": "filename is required"}), 400
    # Secure the filename and generate a unique S3 key
    safe_name = secure_filename(filename)
    file_id = uuid.uuid4().hex  # unique ID
    s3_key = f"{file_id}_{safe_name}"
    content_type = data.get('contentType', 'application/octet-stream')
    try:
        # Generate pre-signed URL for PUT object (valid for 1 hour by default)
        url = s3_client.generate_presigned_url(
            ClientMethod='put_object',
            Params={'Bucket': S3_BUCKET_NAME, 'Key': s3_key, 'ContentType': content_type},
            ExpiresIn=3600  # URL expires in 1 hour (can adjust lower for security)
        )
    except ClientError as e:
        app.logger.error(f"Error generating presigned URL: {e}")
        return jsonify({"error": "Could not generate URL"}), 500
    # Return the URL and the key (the client will use both)
    return jsonify({ "uploadUrl": url, "key": s3_key })

# Endpoint: Confirm upload and save metadata to DB
@app.route('/files/metadata', methods=['POST'])
#@token_required  
def save_file_metadata():
    data = request.get_json()
    file_key = data.get('key')
    filename = data.get('filename')
    if not file_key or not filename:
        return jsonify({"error": "key and filename required"}), 400
    timestamp = int(time.time())
    # Additional metadata fields can be included (e.g., file size, user, etc.)
    item = {
        'FileKey': file_key,
        'FileName': filename,
        'UploadTime': timestamp
    }
    try:
        metadata_table.put_item(Item=item)
    except ClientError as e:
        app.logger.error(f"Error saving metadata: {e}")
        return jsonify({"error": "Could not save metadata"}), 500
    return jsonify({"message": "Metadata saved", "fileId": file_key}), 200

# Endpoint: List all uploaded files' metadata
@app.route('/files', methods=['GET'])
#@token_required
def list_files():
    try:
        response = metadata_table.scan()
        items = response.get('Items', [])
    except Exception as e:
        app.logger.error(f"Error reading metadata: {e}")
        # Return detailed error for debugging (remove in production)
        return jsonify({"error": str(e)}), 500
    return jsonify(items), 200

# Endpoint: Get a download link (pre-signed GET URL) for a specific file
@app.route('/files/<file_id>/download', methods=['GET'])
#@token_required  # (optional, or allow public download if desired)
def get_download_link(file_id):
    # In this simple design, file_id is actually the S3 object key
    s3_key = file_id  
    # (If file_id were separate from S3 key, we'd look up the key in DynamoDB here)
    try:
        url = s3_client.generate_presigned_url(
            ClientMethod='get_object',
            Params={'Bucket': S3_BUCKET_NAME, 'Key': s3_key},
            ExpiresIn=3600  # e.g., 1 hour download link
        )
    except ClientError as e:
        app.logger.error(f"Error generating download URL: {e}")
        return jsonify({"error": "Could not generate download link"}), 500
    # Option 1: Return the URL for the frontend to use
    return jsonify({ "url": url })

if __name__ == '__main__':
    app.run(debug=True, port=5001)
