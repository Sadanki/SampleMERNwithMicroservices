import boto3
import base64
import time
from botocore.exceptions import ClientError

# AWS clients
ec2 = boto3.client('ec2')
autoscaling = boto3.client('autoscaling')

# Constants
SG_ID = 'sg-03cafb6771b41c289'  # ✅ Correct SG in correct VPC
SUBNETS = ['subnet-0c427fea428b48edf', 'subnet-0b98ced52514f8206']
ECR_IMAGE = '975050024946.dkr.ecr.ap-south-1.amazonaws.com/mern-profile-service:latest'
KEY_NAME = 'vignesh-mern-key'  # Your EC2 key pair

# Dynamic names
timestamp = time.strftime('%Y%m%d%H%M%S')
LT_NAME = f'vignesh-backend-launch-template-{timestamp}'
ASG_NAME = f'vignesh-backend-asg-{timestamp}'

def create_launch_template():
    user_data_script = f"""#!/bin/bash
yum update -y
amazon-linux-extras install docker -y
service docker start
usermod -a -G docker ec2-user
docker run -d -p 3002:3002 -e PORT=3002 {ECR_IMAGE}

"""

    encoded_user_data = base64.b64encode(user_data_script.encode('utf-8')).decode('utf-8')

    try:
        response = ec2.create_launch_template(
            LaunchTemplateName=LT_NAME,
            LaunchTemplateData={
                'ImageId': 'ami-0a0f1259dd1c90938',  # Amazon Linux 2 (ap-south-1)
                'InstanceType': 't2.micro',
                'KeyName': KEY_NAME,
                'SecurityGroupIds': [SG_ID],
                'UserData': encoded_user_data
            }
        )
        lt_id = response['LaunchTemplate']['LaunchTemplateId']
        print(f"✅ Launch Template created: {LT_NAME} (ID: {lt_id})")
        return lt_id
    except ClientError as e:
        print(f"❌ Failed to create Launch Template: {e}")
        return None

def create_auto_scaling_group(lt_id):
    try:
        autoscaling.create_auto_scaling_group(
            AutoScalingGroupName=ASG_NAME,
            LaunchTemplate={
                'LaunchTemplateId': lt_id,
                'Version': '$Latest'
            },
            MinSize=1,
            MaxSize=2,
            DesiredCapacity=1,
            VPCZoneIdentifier=",".join(SUBNETS),
            Tags=[{
                'ResourceId': ASG_NAME,
                'ResourceType': 'auto-scaling-group',
                'Key': 'Name',
                'Value': 'vignesh-backend-instance',
                'PropagateAtLaunch': True
            }]
        )
        print(f"✅ Auto Scaling Group created: {ASG_NAME}")
    except ClientError as e:
        print(f"❌ Failed to create ASG: {e}")

if __name__ == "__main__":
    lt_id = create_launch_template()
    if lt_id:
        create_auto_scaling_group(lt_id)
