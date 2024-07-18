import boto3
import os
import subprocess
from dotenv import load_dotenv

# Loading the environment variables from a .env file
load_dotenv()

# Access environment variables
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION')
VPC_ID = os.getenv('VPC_ID')
KEY_NAME = os.getenv('KEY_NAME')
IAM_ROLE = os.getenv('IAM_ROLE')

# Initialize Boto3 clients with specified region
ec2 = boto3.client('ec2', region_name=AWS_REGION)
s3 = boto3.client('s3', region_name=AWS_REGION)
ec2_resource = boto3.resource('ec2', region_name=AWS_REGION)

# Create Security Group
def create_security_group(group_name, description, vpc_id):
    response = ec2.create_security_group(
        GroupName=group_name,
        Description=description,
        VpcId=vpc_id
    )
    security_group_id = response['GroupId']
    ec2.authorize_security_group_ingress(
        GroupId=security_group_id,
        IpPermissions=[
            { 'IpProtocol': 'tcp','FromPort': 22, 'ToPort': 22, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
            {'IpProtocol': 'tcp', 'FromPort': 80, 'ToPort': 80, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
            {'IpProtocol': 'tcp', 'FromPort': 443, 'ToPort': 443, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
            {'IpProtocol': 'tcp', 'FromPort': 8000, 'ToPort': 8000, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
            {'IpProtocol': 'tcp', 'FromPort': 5432, 'ToPort': 5432, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
        ]
    )
    return security_group_id

# Create EC2 instance
def create_ec2_instance(security_group_id):
    instances = ec2_resource.create_instances(
        ImageId='ami-0b72821e2f351e396',
        MinCount=1,
        MaxCount=1,
        InstanceType='t2.micro',
        KeyName=KEY_NAME,
        SecurityGroupIds=[security_group_id],
        UserData=open('ec2_user_data.sh').read(),
        IamInstanceProfile={'Name': IAM_ROLE},
    )
    instance_id = instances[0].id
    print(f'Created EC2 instance: {instance_id}')

    # Wait for the instance to be in the running state
    instance = ec2_resource.Instance(instance_id)
    instance.wait_until_running()
    print(f'EC2 instance is running: {instance_id}')

    return instance_id

# Allocate and associate Elastic IP
def create_and_link_eip(instance_id):
    allocation = ec2.allocate_address(Domain='vpc')
    eip_allocation_id = allocation['AllocationId']
    eip_public_ip = allocation['PublicIp']
    ec2.associate_address(
        InstanceId=instance_id,
        AllocationId=eip_allocation_id
    )
    print(f'Elastic IP {eip_public_ip} allocated and associated with instance {instance_id}')
    return eip_public_ip

# Main script
group_name = 'recipeapi-sg'
description = 'Security group for Recipe API Django application'

security_group_id = create_security_group(group_name, description, VPC_ID)
ec2_instance = create_ec2_instance(security_group_id)
eip_public_ip = create_and_link_eip(ec2_instance)

print(f'EC2 instance created: {ec2_instance}')
print(f'Elastic IP allocated: {eip_public_ip}')

