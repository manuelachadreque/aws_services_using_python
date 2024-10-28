"""
this script manages amazon EC2 instances using Boto3 Python SDK

"""

import boto3

#create sc2 resources and instance name
ec2=boto3.resource('ec2', region_name='eu-west-2')
instance_name='manu-ec2-hol'

#store instance id

instance_id=None


#check if instance whicj you are trying to create alreadyexists 
#and only work with an instance that hasn't been terminated
#lounch a new EC2 instance if it hasn't already been created
instances = ec2.instances.all()
instance_exists =False

for instance in instances:
    for tag in instance.tags:
        if tag['Key'] =='Name' and tag['Value'] == instance_name:
            instance_exists =True
            instance_id = instance.id
            print(f"An instance named ' {instance_name} with id '{instance_id} already exists.")
            break
    if instance_exists:
        break

if not instance_exists:
    new_instance =ec2.create_instances(
        ImageId='ami-03c6b308140d10488',
        MinCount =1,
        MaxCount =1,
        InstanceType='t2.micro',
        KeyName = 'manu-ec2',
        TagSpecifications =[
        {
                'ResourceType': 'instance',
                'Tags':[
                    {'Key':'Name',
                    'Value':instance_name
                    },
                ]
        },
        ]

        )
    instance_id=new_instance[0].id
    print(f"instance named '{instance_name}' with id '{instance_id}' created.")


#stop an instance
ec2.Instance(instance_id).stop()
print(f"instance ' {instance_name}-{instance_id}' stopped.")

#Start an instance

ec2.Instance(instance_id).start()
print(f"instance ' {instance_name}-{instance_id}' started.")


