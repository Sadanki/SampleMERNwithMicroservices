import boto3
import base64
from botocore.exceptions import ClientError

# AWS clients
ec2 = boto3.client('ec2')
autoscaling = boto3.client('autoscaling')

# Constants
SG_ID = 'sg-0049a9b2a1b873e12'
SUBNETS = ['subnet-06809382ba312a3e6', 'subnet-08a74f859fdd685cf']  # ✅ public subnets
ECR_IMAGE = '975050024946.dkr.ecr.ap-south-1.amazonaws.com/mern-profile-service:latest'

def create_launch_template():
    user_data_script = f"""#!/bin/bash
yum update -y
amazon-linux-extras install docker -y
service docker start
usermod -a -G docker ec2-user
docker run -d -p 3001:3001 {ECR_IMAGE}
"""

    encoded_user_data = base64.b64encode(user_data_script.encode('utf-8')).decode('utf-8')

    try:
        response = ec2.create_launch_template(
            LaunchTemplateName='mern-backend-launch-template-v4',
            LaunchTemplateData={
                'ImageId': 'ami-03f4878755434977f',  # Amazon Linux 2 in ap-south-1
                'InstanceType': 't2.micro',
                'SecurityGroupIds': [SG_ID],
                'UserData': encoded_user_data
            }
        )
        lt_id = response['LaunchTemplate']['LaunchTemplateId']
        print(f"✅ Launch Template created: {lt_id}")
        return lt_id
    except ClientError as e:
        print(f"❌ Failed to create Launch Template: {e}")
        return None

def create_auto_scaling_group(lt_id):
    try:
        autoscaling.create_auto_scaling_group(
            AutoScalingGroupName='mern-backend-asg-v4',
            LaunchTemplate={
                'LaunchTemplateId': lt_id,
                'Version': '$Latest'
            },
            MinSize=1,
            MaxSize=2,
            DesiredCapacity=1,
            VPCZoneIdentifier=",".join(SUBNETS),
            Tags=[{
                'ResourceId': 'mern-backend-asg-v4',
                'ResourceType': 'auto-scaling-group',
                'Key': 'Name',
                'Value': 'mern-backend-instance-v4',
                'PropagateAtLaunch': True
            }]
        )
        print("✅ Auto Scaling Group created.")
    except ClientError as e:
        print(f"❌ Failed to create ASG: {e}")

if __name__ == "__main__":
    lt_id = create_launch_template()
    if lt_id:
        create_auto_scaling_group(lt_id)
