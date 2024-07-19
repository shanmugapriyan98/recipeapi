import boto3
import json
import os
from dotenv import load_dotenv

# Loading the environment variables from a .env file
load_dotenv()

# Access environment variables
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION')

# Initialize Boto3 clients
ec2 = boto3.client('ec2', region_name=AWS_REGION)
ec2_resource = boto3.resource('ec2', region_name=AWS_REGION)

# File to read resource IDs from
ID_FILE = 'resource_ids.json'

def read_ids_from_file():
    with open(ID_FILE, 'r') as f:
        ids = json.load(f)
    print(f'Read resource IDs from {ID_FILE}')
    return ids

# Terminate EC2 Instance
def terminate_ec2_instance(instance_id):
    ec2_resource.Instance(instance_id).terminate()
    print(f'Terminating EC2 instance: {instance_id}')
    ec2_resource.Instance(instance_id).wait_until_terminated()
    print(f'EC2 instance terminated: {instance_id}')

# Release Elastic IP
def release_elastic_ip(allocation_id):
    ec2.release_address(AllocationId=allocation_id)
    print(f'Released Elastic IP with Allocation ID: {allocation_id}')

# Delete Security Group
def delete_security_group(security_group_id):
    ec2.delete_security_group(GroupId=security_group_id)
    print(f'Deleted Security Group: {security_group_id}')

# Detach and Delete Internet Gateway
def delete_internet_gateway(vpc_id, igw_id):
    ec2.detach_internet_gateway(InternetGatewayId=igw_id, VpcId=vpc_id)
    ec2.delete_internet_gateway(InternetGatewayId=igw_id)
    print(f'Deleted Internet Gateway: {igw_id}')

# Delete Route Table
def delete_route_table(route_table_id):
    ec2.delete_route_table(RouteTableId=route_table_id)
    print(f'Deleted Route Table: {route_table_id}')

# Delete Subnet
def delete_subnet(subnet_id):
    ec2.delete_subnet(SubnetId=subnet_id)
    print(f'Deleted Subnet: {subnet_id}')

# Delete VPC
def delete_vpc(vpc_id):
    ec2.delete_vpc(VpcId=vpc_id)
    print(f'Deleted VPC: {vpc_id}')


ids = read_ids_from_file()

terminate_ec2_instance(ids['instance_id'])
delete_security_group(ids['security_group_id'])
delete_internet_gateway(ids['vpc_id'], ids['igw_id'])
delete_subnet(ids['subnet_id'])
delete_route_table(ids['route_table_id'])
release_elastic_ip(ids['eip_allocation_id'])
delete_vpc(ids['vpc_id'])

