import boto3

# instantiate a boto3 resource fors3 and name your bucket
s3 = boto3.resource('s3')
bucket_name='manuela-aws-python-dct-crud'
region ='eu-west-2'


#check if bucket exists

all_my_buckets = [bucket.name for bucket in s3.buckets.all()]
print(all_my_buckets)

if bucket_name not in all_my_buckets:
    print(f"'{bucket_name}' bucket name does not exists creating now...")
    s3.create_bucket(
    Bucket=bucket_name,
    CreateBucketConfiguration={
        'LocationConstraint': 'eu-west-2',
    },
)

    print(f"'{bucket_name} has been created.")
else:
    print(f"{bucket_name} bucket already exists. no need to createa new one. ")
#create 'file_1' and 'file_2'
file_1='file_1.txt'
file_2='file_2.txt'

#upload file_1 and file_2
s3.Bucket(bucket_name).upload_file(Filename=file_1, Key=file_1)


#Read and print the file from bucket
obj=s3.Object(bucket_name,file_1)
body=obj.get()['Body'].read()
print(body)

#Update 'file_1' in the bucket with new content from file_2

s3.Object(bucket_name,file_1).put(Body=open(file_2,'rb'))

obj=s3.Object(bucket_name,file_1)
body=obj.get()['Body'].read()
print(body)
#Delete the file from bucket
s3.Object(bucket_name,file_1).delete()


# delete the bucket (the bucket shut be empty)
bucket=s3.Bucket(bucket_name)
bucket.delete()