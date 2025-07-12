import boto3

ec2 = boto3.client('ec2')

vpc_id = 'vpc-074a3dcc782c93eb0'

def create_public_subnet(cidr_block, az, name):
    response = ec2.create_subnet(
        VpcId=vpc_id,
        CidrBlock=cidr_block,
        AvailabilityZone=az,
        TagSpecifications=[{
            'ResourceType': 'subnet',
            'Tags': [{'Key': 'Name', 'Value': name}]
        }]
    )
    subnet_id = response['Subnet']['SubnetId']
    print(f"✅ Subnet created: {subnet_id}")

    # Enable auto-assign public IP
    ec2.modify_subnet_attribute(
        SubnetId=subnet_id,
        MapPublicIpOnLaunch={'Value': True}
    )
    print(f"🔓 Enabled public IP auto-assign for {subnet_id}")
    return subnet_id

if __name__ == "__main__":
    subnet1 = create_public_subnet('10.0.3.0/24', 'ap-south-1a', 'public-subnet-1')
    subnet2 = create_public_subnet('10.0.4.0/24', 'ap-south-1b', 'public-subnet-2')
    print(f"\n🎉 New public subnets created:\n - {subnet1}\n - {subnet2}")
