import boto3
import base64

ec2 = boto3.client('ec2', region_name='ap-south-1')

user_data = '''#!/bin/bash
sudo yum update -y
sudo yum install docker -y
sudo service docker start
sudo usermod -aG docker ec2-user
docker login -u AWS -p $(aws ecr get-login-password --region ap-south-1) 975050024946.dkr.ecr.ap-south-1.amazonaws.com
docker run -d -p 3001:3001 -e PORT=3001 975050024946.dkr.ecr.ap-south-1.amazonaws.com/mern-hello-service:latest
'''
encoded_user_data = base64.b64encode(user_data.encode('utf-8')).decode('utf-8')

response = ec2.create_launch_template(
    LaunchTemplateName='vignesh-hello-launch-template',
    LaunchTemplateData={
        'ImageId': 'ami-0c42696027a8ede58',
        'InstanceType': 't2.micro',
        'KeyName': 'vignesh-mern-key',
        'SecurityGroupIds': ['sg-069bc2d78cd3ad29a'],  # Must belong to VPC vpc-0056d809452f9f8ea
        'UserData': encoded_user_data
    }
)
print("✅ Launch Template ID:", response['LaunchTemplate']['LaunchTemplateId'])
