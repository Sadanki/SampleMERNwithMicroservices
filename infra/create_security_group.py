import boto3

ec2 = boto3.client('ec2')

VPC_ID = 'vpc-074a3dcc782c93eb0'  # Use your actual VPC ID

def create_security_group():
    try:
        response = ec2.create_security_group(
            GroupName='mern-backend-sg',
            Description='Allow SSH, HTTP, and App port',
            VpcId=VPC_ID
        )
        sg_id = response['GroupId']
        print(f"Security Group Created: {sg_id}")

        # Add inbound rules
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
                    'FromPort': 80,
                    'ToPort': 80,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                },
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 3001,  # Replace with your app port if different
                    'ToPort': 3001,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                }
            ]
        )

        print("Inbound rules added.")
        return sg_id

    except Exception as e:
        print("Error creating security group:", e)

if __name__ == "__main__":
    create_security_group()
