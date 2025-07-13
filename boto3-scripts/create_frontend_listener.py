import boto3

elbv2 = boto3.client('elbv2', region_name='ap-south-1')

response = elbv2.create_listener(
    LoadBalancerArn='arn:aws:elasticloadbalancing:ap-south-1:975050024946:loadbalancer/app/vignesh-frontend-alb3/36f35b86708a0c37',
    Protocol='HTTP',
    Port=80,
    DefaultActions=[
        {
            'Type': 'forward',
            'TargetGroupArn': 'arn:aws:elasticloadbalancing:ap-south-1:975050024946:targetgroup/vignesh-frontend-tg/742965a6e18b061c'
        }
    ]
)

print("✅ Listener for frontend ALB created successfully.")
