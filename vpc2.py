import boto3

# Initialize the EC2 client
ec2 = boto3.client('ec2')

# Define VPC and Internet Gateway names
vpc_name = 'vpc-hol'
ig_name = 'ig-vpc-hol'

# Find the VPC
vpcs = ec2.describe_vpcs(Filters=[{'Name': 'tag:Name', 'Values': [vpc_name]}]).get('Vpcs', [])

if vpcs:
    vpc_id = vpcs[0]['VpcId']
    print(f"Deleting VPC '{vpc_name}' with ID '{vpc_id}'...")

    # Find and detach the Internet Gateway
    internet_gateways = ec2.describe_internet_gateways(Filters=[{'Name': 'tag:Name', 'Values': [ig_name]}]).get('InternetGateways', [])
    if internet_gateways:
        ig_id = internet_gateways[0]['InternetGatewayId']
        print(f"Detaching Internet Gateway '{ig_name}' with ID '{ig_id}' from VPC...")
        ec2.detach_internet_gateway(VpcId=vpc_id, InternetGatewayId=ig_id)

        print(f"Deleting Internet Gateway '{ig_name}'...")
        ec2.delete_internet_gateway(InternetGatewayId=ig_id)

    # Find and delete Subnets
    subnets = ec2.describe_subnets(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}]).get('Subnets', [])
    for subnet in subnets:
        subnet_id = subnet['SubnetId']
        print(f"Deleting Subnet with ID '{subnet_id}'...")
        ec2.delete_subnet(SubnetId=subnet_id)

    # Find and delete Route Tables
    route_tables = ec2.describe_route_tables(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}]).get('RouteTables', [])
    for rt in route_tables:
        rt_id = rt['RouteTableId']
        if rt['Associations']:
            for association in rt['Associations']:



