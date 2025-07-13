import boto3

elbv2 = boto3.client('elbv2', region_name='ap-south-1')

response = elbv2.create_target_group(
    Name='vignesh-hello-tg2',
    Protocol='HTTP',
    Port=3001,
    VpcId='vpc-0056d809452f9f8ea',
    TargetType='instance'
)

print("✅ Target Group ARN:", response['TargetGroups'][0]['TargetGroupArn'])
