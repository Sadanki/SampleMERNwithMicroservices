import boto3

elbv2 = boto3.client('elbv2', region_name='ap-south-1')

response = elbv2.create_load_balancer(
    Name='v-hello-alb',
    Subnets=[
        'subnet-066ec2d046612e19b',  # ap-south-1c
        'subnet-0c1842aca7dc1b6b0'   # ap-south-1b
    ],
    SecurityGroups=[
        'sg-069bc2d78cd3ad29a'  # Must match the VPC
    ],
    Scheme='internet-facing',
    Tags=[{'Key': 'Name', 'Value': 'v-hello-alb'}],
    Type='application',
    IpAddressType='ipv4'
)

dns = response['LoadBalancers'][0]['DNSName']
print("✅ ALB DNS:", dns)
