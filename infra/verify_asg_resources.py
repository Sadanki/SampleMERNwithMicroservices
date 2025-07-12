import boto3

ec2 = boto3.client('ec2')
asg = boto3.client('autoscaling')

def check_launch_template():
    response = ec2.describe_launch_templates(
        Filters=[{'Name': 'launch-template-name', 'Values': ['mern-backend-launch-template']}]
    )
    if response['LaunchTemplates']:
        print("✅ Launch Template exists.")
    else:
        print("❌ Launch Template NOT found.")

def check_asg():
    response = asg.describe_auto_scaling_groups(
        AutoScalingGroupNames=['mern-backend-asg']
    )
    if response['AutoScalingGroups']:
        print("✅ Auto Scaling Group exists.")
        instances = response['AutoScalingGroups'][0]['Instances']
        if instances:
            print(f"✅ ASG has {len(instances)} EC2 instance(s) running:")
            for inst in instances:
                print(f"   - Instance ID: {inst['InstanceId']}, Lifecycle: {inst['LifecycleState']}")
        else:
            print("⚠️ ASG has no running instances.")
    else:
        print("❌ Auto Scaling Group NOT found.")

if __name__ == "__main__":
    check_launch_template()
    check_asg()
