import boto3

ec2 = boto3.client('ec2')

def create_vpc():
    # Create VPC
    vpc = ec2.create_vpc(CidrBlock='10.0.0.0/16')
    vpc_id = vpc['Vpc']['VpcId']
    ec2.modify_vpc_attribute(VpcId=vpc_id, EnableDnsSupport={'Value': True})
    ec2.modify_vpc_attribute(VpcId=vpc_id, EnableDnsHostnames={'Value': True})
    print(f"VPC created: {vpc_id}")

    # Create Internet Gateway and attach to VPC
    igw = ec2.create_internet_gateway()
    igw_id = igw['InternetGateway']['InternetGatewayId']
    ec2.attach_internet_gateway(VpcId=vpc_id, InternetGatewayId=igw_id)
    print(f"Internet Gateway created: {igw_id}")

    # Create Public Subnet
    subnet1 = ec2.create_subnet(CidrBlock='10.0.1.0/24', VpcId=vpc_id, AvailabilityZone='ap-south-1a')
    subnet2 = ec2.create_subnet(CidrBlock='10.0.2.0/24', VpcId=vpc_id, AvailabilityZone='ap-south-1b')
    print(f"Subnets created: {subnet1['Subnet']['SubnetId']}, {subnet2['Subnet']['SubnetId']}")

    # Create Route Table and Route
    rt = ec2.create_route_table(VpcId=vpc_id)
    rt_id = rt['RouteTable']['RouteTableId']
    ec2.create_route(RouteTableId=rt_id, DestinationCidrBlock='0.0.0.0/0', GatewayId=igw_id)
    ec2.associate_route_table(RouteTableId=rt_id, SubnetId=subnet1['Subnet']['SubnetId'])
    ec2.associate_route_table(RouteTableId=rt_id, SubnetId=subnet2['Subnet']['SubnetId'])

    print("Route table and routing configured.")

    return vpc_id, [subnet1['Subnet']['SubnetId'], subnet2['Subnet']['SubnetId']], igw_id

if __name__ == "__main__":
    create_vpc()
