import boto3
import time

# Initialize Boto3 clients
elbv2 = boto3.client('elbv2')
autoscaling = boto3.client('autoscaling')

# ✅ Replace with your actual values
VPC_ID = 'vpc-058e382dbeb42b136'
SUBNETS = ['subnet-0c427fea428b48edf', 'subnet-0b98ced52514f8206']
SG_ID = 'sg-03cafb6771b41c289'
ASG_NAME = 'vignesh-backend-asg-20250713001543'
PORT = 3002  # Port used by profileService

# Generate timestamp and valid AWS names
timestamp = time.strftime('%Y%m%d%H%M%S')
TG_NAME = f'v-b-tg-{timestamp}'              # ✅ Short name (max 32 chars)
ALB_NAME = f'v-b-alb-{timestamp}'            # ALB allows 32 chars, this is fine

def create_target_group():
    response = elbv2.create_target_group(
        Name=TG_NAME,
        Protocol='HTTP',
        Port=PORT,
        VpcId=VPC_ID,
        TargetType='instance',
        HealthCheckProtocol='HTTP',
        HealthCheckPort=str(PORT),
        HealthCheckPath='/health',
        Matcher={'HttpCode': '200'}
    )
    tg_arn = response['TargetGroups'][0]['TargetGroupArn']
    print(f"✅ Target Group created: {TG_NAME} (ARN: {tg_arn})")
    return tg_arn

def create_alb(tg_arn):
    response = elbv2.create_load_balancer(
        Name=ALB_NAME,
        Subnets=SUBNETS,
        SecurityGroups=[SG_ID],
        Scheme='internet-facing',
        Type='application',
        IpAddressType='ipv4'
    )
    lb_arn = response['LoadBalancers'][0]['LoadBalancerArn']
    lb_dns = response['LoadBalancers'][0]['DNSName']
    print(f"✅ ALB created: {ALB_NAME} ({lb_dns})")

    # Wait until ALB is active
    waiter = elbv2.get_waiter('load_balancer_available')
    print("⏳ Waiting for ALB to become active...")
    waiter.wait(LoadBalancerArns=[lb_arn])
    print("✅ ALB is now active.")

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
    print("✅ Listener created on port 80.")
    return lb_dns

def attach_asg_to_target_group(tg_arn):
    autoscaling.attach_load_balancer_target_groups(
        AutoScalingGroupName=ASG_NAME,
        TargetGroupARNs=[tg_arn]
    )
    print(f"✅ Target Group attached to ASG: {ASG_NAME}")

if __name__ == "__main__":
    tg_arn = create_target_group()
    alb_dns = create_alb(tg_arn)
    attach_asg_to_target_group(tg_arn)

    print(f"\n🌐 Access your profileService at: http://{alb_dns}")
