import boto3
import os
from dotenv import load_dotenv

# Loading the environment variables from a .env file
load_dotenv()

# Access environment variables
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION')
KEY_NAME = os.getenv('KEY_NAME')
IAM_ROLE = os.getenv('IAM_ROLE')

# Initialize Boto3 clients
ec2 = boto3.client('ec2', region_name=AWS_REGION)
ec2_resource = boto3.resource('ec2', region_name=AWS_REGION)

# Create VPC
def create_vpc():
    vpc = ec2_resource.create_vpc(CidrBlock='10.0.0.0/16')
    vpc.wait_until_available()
    vpc.create_tags(Tags=[{"Key": "Name", "Value": "recipeapi_vpc"}])
    print(f'VPC created: {vpc.id}')
    return vpc

# Create Subnet
def create_subnet(vpc):
    subnet = ec2_resource.create_subnet(CidrBlock='10.0.1.0/24', VpcId=vpc.id)
    subnet.create_tags(Tags=[{"Key": "Name", "Value": "recipeapi_subnet"}])
    print(f'Subnet created: {subnet.id}')
    return subnet

# Create Internet Gateway and attach it to the VPC
def create_internet_gateway(vpc):
    igw = ec2_resource.create_internet_gateway()
    igw.attach_to_vpc(VpcId=vpc.id)
    vpc.modify_attribute(EnableDnsHostnames={'Value': True})
    vpc.modify_attribute(EnableDnsSupport={'Value': True})
    print(f'Internet Gateway created and attached: {igw.id}')
    return igw

# Create Route Table and add a route to the Internet Gateway
def create_route_table(vpc, igw, subnet):
    route_table = ec2_resource.create_route_table(VpcId=vpc.id)
    route_table.create_tags(Tags=[{"Key": "Name", "Value": "recipeapi_route_table"}])
    route_table.create_route(
        DestinationCidrBlock='0.0.0.0/0',
        GatewayId=igw.id
    )
    route_table.associate_with_subnet(SubnetId=subnet.id)
    print(f'Route Table created and associated with subnet: {route_table.id}')
    return route_table

# Create Security Group
def create_security_group(group_name, description, vpc):
    security_group = ec2_resource.create_security_group(
        GroupName=group_name,
        Description=description,
        VpcId=vpc.id
    )
    security_group.authorize_ingress(
        IpPermissions=[
            {'IpProtocol': 'tcp', 'FromPort': 22, 'ToPort': 22, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
            {'IpProtocol': 'tcp', 'FromPort': 80, 'ToPort': 80, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
            {'IpProtocol': 'tcp', 'FromPort': 443, 'ToPort': 443, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
            {'IpProtocol': 'tcp', 'FromPort': 8000, 'ToPort': 8000, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
            {'IpProtocol': 'tcp', 'FromPort': 5432, 'ToPort': 5432, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
        ]
    )
    print(f'Security Group created: {security_group.id}')
    return security_group

# Create EC2 instance
def create_ec2_instance(subnet, security_group):
    instances = ec2_resource.create_instances(
        ImageId='ami-0b72821e2f351e396',  # Replace with your desired AMI ID
        MinCount=1,
        MaxCount=1,
        NetworkInterfaces=[{
            'SubnetId': subnet.id,
            'DeviceIndex': 0,
            'AssociatePublicIpAddress': True,
            'Groups': [security_group.id]
        }],
        InstanceType='t2.micro',
        KeyName=KEY_NAME,
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

# Create VPC
vpc = create_vpc()
# Create Subnet
subnet = create_subnet(vpc)
# Create Internet Gateway
igw = create_internet_gateway(vpc)
# Create Route Table and add a route to the Internet Gateway
create_route_table(vpc, igw, subnet)
# Create Security Group
security_group = create_security_group(group_name, description, vpc)
# Create EC2 Instance
ec2_instance = create_ec2_instance(subnet, security_group)
# Allocate and Associate Elastic IP
eip_public_ip = create_and_link_eip(ec2_instance)

print(f'EC2 instance created: {ec2_instance}')
print(f'Elastic IP allocated: {eip_public_ip}')