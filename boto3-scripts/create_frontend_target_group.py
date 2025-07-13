import boto3

elbv2 = boto3.client('elbv2', region_name='ap-south-1')

response = elbv2.create_target_group(
    Name='vignesh-frontend-tg',
    Protocol='HTTP',
    Port=80,
    VpcId='vpc-0056d809452f9f8ea',  # ✅ Use your actual VPC ID
    TargetType='instance',
    HealthCheckProtocol='HTTP',
    HealthCheckPort='80',
    HealthCheckPath='/',
    HealthCheckIntervalSeconds=30,
    HealthCheckTimeoutSeconds=5,
    HealthyThresholdCount=2,
    UnhealthyThresholdCount=2,
    Matcher={
        'HttpCode': '200'
    }
)

print("✅ Target Group ARN:", response['TargetGroups'][0]['TargetGroupArn'])
