import boto3

autoscaling = boto3.client('autoscaling', region_name='ap-south-1')

response = autoscaling.create_auto_scaling_group(
    AutoScalingGroupName='vignesh-hello-asg',
    LaunchTemplate={
        'LaunchTemplateName': 'vignesh-hello-launch-template',
        'Version': '$Latest'
    },
    MinSize=1,
    MaxSize=2,
    DesiredCapacity=1,
    VPCZoneIdentifier='subnet-066ec2d046612e19b,subnet-0c1842aca7dc1b6b0',
    TargetGroupARNs=[
        'arn:aws:elasticloadbalancing:ap-south-1:975050024946:targetgroup/vignesh-hello-tg/9fba635a339b901c'
    ]
)

print("✅ Auto Scaling Group created successfully.")
