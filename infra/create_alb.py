import boto3
import time

# Initialize Boto3 clients
elbv2 = boto3.client('elbv2')
autoscaling = boto3.client('autoscaling')
ec2 = boto3.client('ec2')

# Constants (replace with your IDs)
VPC_ID = 'vpc-074a3dcc782c93eb0'
SUBNETS = ['subnet-0f55305c7ef937743', 'subnet-00e3c2eb9a879075e']
SG_ID = 'sg-0049a9b2a1b873e12'
ASG_NAME = 'mern-backend-asg'

def create_target_group():
    response = elbv2.create_target_group(
        Name='mern-backend-tg',
        Protocol='HTTP',
        Port=3001,
        VpcId=VPC_ID,
        TargetType='instance',
        HealthCheckProtocol='HTTP',
        HealthCheckPort='3001',
        HealthCheckPath='/health',
        Matcher={'HttpCode': '200'}
    )
    tg_arn = response['TargetGroups'][0]['TargetGroupArn']
    print(f"✅ Target Group created: {tg_arn}")
    return tg_arn

def create_alb(tg_arn):
    response = elbv2.create_load_balancer(
        Name='mern-backend-alb',
        Subnets=SUBNETS,
        SecurityGroups=[SG_ID],
        Scheme='internet-facing',
        Type='application',
        IpAddressType='ipv4'
    )
    lb_arn = response['LoadBalancers'][0]['LoadBalancerArn']
    lb_dns = response['LoadBalancers'][0]['DNSName']
    print(f"✅ ALB created: {lb_dns}")

    # Wait for ALB to become active
    print("⏳ Waiting for ALB to become active...")
    waiter = elbv2.get_waiter('load_balancer_available')
    waiter.wait(LoadBalancerArns=[lb_arn])
    print("✅ ALB is active!")

    # Create Listener
    elbv2.create_listener(
        LoadBalancerArn=lb_arn,
        Protocol='HTTP',
        Port=80,
        DefaultActions=[{
            'Type': 'forward',
            'TargetGroupArn': tg_arn
        }]
    )
    print("✅ Listener created on port 80")
    return lb_dns

def attach_asg_to_target_group(tg_arn):
    autoscaling.attach_load_balancer_target_groups(
        AutoScalingGroupName=ASG_NAME,
        TargetGroupARNs=[tg_arn]
    )
    print("✅ Target Group attached to ASG")

if __name__ == "__main__":
    tg_arn = create_target_group()
    alb_dns = create_alb(tg_arn)
    attach_asg_to_target_group(tg_arn)

    print(f"\n🌐 Access your app using the ALB DNS: http://{alb_dns}")
