import boto3
import os
import datetime
import subprocess

def lambda_handler(event, context):
    # Set variables
    db_name = os.environ.get('DB_NAME', 'mern-profile-db')
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    backup_file = f"/tmp/{db_name}-{timestamp}.gz"
    s3_bucket = os.environ.get('S3_BUCKET', 'vignesh-db-backup-bucket')
    s3_key = f"mongo-backups/{db_name}-{timestamp}.gz"

    # Run mongodump (Mongo must be accessible from Lambda — e.g. hosted on EC2 or Atlas with open IP)
    try:
        subprocess.run([
            "mongodump",
            f"--uri={os.environ['MONGO_URI']}",
            "--archive=" + backup_file,
            "--gzip"
        ], check=True)

        # Upload to S3
        s3 = boto3.client('s3')
        s3.upload_file(backup_file, s3_bucket, s3_key)

        return {
            'statusCode': 200,
            'body': f"Backup successful and uploaded to s3://{s3_bucket}/{s3_key}"
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }
