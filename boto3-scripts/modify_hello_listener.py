import boto3

elbv2 = boto3.client('elbv2', region_name='ap-south-1')

response = elbv2.modify_listener(
    ListenerArn='arn:aws:elasticloadbalancing:ap-south-1:975050024946:listener/app/v-hello-alb/849211a26a363825/c7cbb753c9ba760a',
    DefaultActions=[
        {
            'Type': 'forward',
            'TargetGroupArn': 'arn:aws:elasticloadbalancing:ap-south-1:975050024946:targetgroup/vignesh-hello-tg2/9c1eaff8060083b0'
        }
    ]
)

print("✅ Listener updated to point to vignesh-hello-tg2")
