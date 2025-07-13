import boto3

elbv2 = boto3.client('elbv2', region_name='ap-south-1')

# Replace with your existing listener ARN
listener_arn = 'arn:aws:elasticloadbalancing:ap-south-1:975050024946:listener/app/v-hello-alb/...'

response = elbv2.modify_listener(
    ListenerArn=listener_arn,
    DefaultActions=[
        {
            'Type': 'forward',
            'TargetGroupArn': 'arn:aws:elasticloadbalancing:ap-south-1:975050024946:targetgroup/vignesh-hello-tg2/9c1eaff8060083b0'
        }
    ]
)

print("✅ Listener updated successfully.")
