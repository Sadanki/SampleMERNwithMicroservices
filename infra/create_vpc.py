import boto3
import json

ec2 = boto3.client('ec2')

def create_vpc():
    # Create VPC
    vpc = ec2.create_vpc(CidrBlock='10.0.0.0/16')
    vpc_id = vpc['Vpc']['VpcId']
    ec2.modify_vpc_attribute(VpcId=vpc_id, EnableDnsSupport={'Value': True})
    ec2.modify_vpc_attribute(VpcId=vpc_id, EnableDnsHostnames={'Value': True})
    print(f"✅ VPC created: {vpc_id}")

    # Create Internet Gateway
    igw = ec2.create_internet_gateway()
    igw_id = igw['InternetGateway']['InternetGatewayId']
    ec2.attach_internet_gateway(VpcId=vpc_id, InternetGatewayId=igw_id)
    print(f"🌐 Internet Gateway created: {igw_id}")

    # Create Subnets
    subnet1 = ec2.create_subnet(CidrBlock='10.0.1.0/24', VpcId=vpc_id, AvailabilityZone='ap-south-1a')
    subnet2 = ec2.create_subnet(CidrBlock='10.0.2.0/24', VpcId=vpc_id, AvailabilityZone='ap-south-1b')
    subnet_ids = [subnet1['Subnet']['SubnetId'], subnet2['Subnet']['SubnetId']]
    print(f"🌍 Subnets created: {subnet_ids[0]}, {subnet_ids[1]}")

    # Route table
    rt = ec2.create_route_table(VpcId=vpc_id)
    rt_id = rt['RouteTable']['RouteTableId']
    ec2.create_route(RouteTableId=rt_id, DestinationCidrBlock='0.0.0.0/0', GatewayId=igw_id)
    ec2.associate_route_table(RouteTableId=rt_id, SubnetId=subnet_ids[0])
    ec2.associate_route_table(RouteTableId=rt_id, SubnetId=subnet_ids[1])
    print(f"🧭 Route table configured: {rt_id}")

    # Save for reuse
    with open("vpc_outputs.json", "w") as f:
        json.dump({
            "vpc_id": vpc_id,
            "subnet_ids": subnet_ids,
            "igw_id": igw_id
        }, f)

    return vpc_id, subnet_ids, igw_id

if __name__ == "__main__":
    create_vpc()
