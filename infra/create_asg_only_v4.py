import boto3
from botocore.exceptions import ClientError

autoscaling = boto3.client('autoscaling')

# ✅ Use confirmed public subnets
SUBNETS = ['subnet-06809382ba312a3e6', 'subnet-08a74f859fdd685cf']

def create_auto_scaling_group():
    try:
        autoscaling.create_auto_scaling_group(
            AutoScalingGroupName='mern-backend-asg-v4',
            LaunchTemplate={
                'LaunchTemplateName': 'mern-backend-launch-template-v4',
                'Version': '$Latest'
            },
            MinSize=1,
            MaxSize=2,
            DesiredCapacity=1,
            VPCZoneIdentifier=",".join(SUBNETS),
            Tags=[{
                'ResourceId': 'mern-backend-asg-v4',
                'ResourceType': 'auto-scaling-group',
                'Key': 'Name',
                'Value': 'mern-backend-instance-v4',
                'PropagateAtLaunch': True
            }]
        )
        print("✅ Auto Scaling Group re-created.")
    except ClientError as e:
        print(f"❌ Failed to create ASG: {e}")

if __name__ == "__main__":
    create_auto_scaling_group()
