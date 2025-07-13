import boto3
import json

# Load VPC ID from saved file
with open("vpc_outputs.json") as f:
    data = json.load(f)
vpc_id = data['vpc_id']

ec2 = boto3.client('ec2')

try:
    response = ec2.create_security_group(
        GroupName='vignesh-backend-sg',
        Description='Allow ports for backend',
        VpcId=vpc_id
    )
    sg_id = response['GroupId']
    print(f"✅ Security Group Created: {sg_id}")

    ec2.authorize_security_group_ingress(
        GroupId=sg_id,
        IpPermissions=[
            {
                'IpProtocol': 'tcp',
                'FromPort': 22,
                'ToPort': 22,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
            },
            {
                'IpProtocol': 'tcp',
                'FromPort': 3001,
                'ToPort': 3001,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
            }
        ]
    )
    print("✅ Inbound rules added.")
except Exception as e:
    print(f"❌ Error creating security group: {e}")
