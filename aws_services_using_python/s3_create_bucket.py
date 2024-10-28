import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError


def create_aws_connection(aws_access_key_id, aws_secret_access_key, region):
    connection_sucessful=False
    s3 = boto3.resource( 's3',
                      aws_access_key_id=aws_access_key_id,
                      aws_secret_access_key=aws_secret_access_key,
                      region_name=region
                      )
    try:
        s3.meta.client.list_buckets()
        connection_sucessful=True
        print("connection was sucessfull")
    except (NoCredentialsError, PartialCredentialsError):
        print("Invalid or incomplete credentials provided.")
    except ClientError as e:
        print("Failed to connect to AWS s3", e)
    return None


def create_new_bucket(s3, bucket_name):


    # check if bucket exists
    all_my_buckets =[bucket.name for bucket in s3.buckets.all()]
    print(all_my_buckets)

    if bucket_name not in all_my_buckets:
        s3.create_bucket(
            Bucket =bucket_name,
            CreateBucketConfiguration={
                'LocationConstraint': s3.region
            },
        )
        print(f"'{bucket_name} has beeen created.")

    else:
        print(f"'{bucket_name} bucket already exists. no need to create a new one.")



def upload_files(s3, bucket_name, file_name):
    s3.Bucket(bucket_name).upload_file(Filename=file_name, Key=file_name)


def read_file(s3, bucket_name,file_name):
    obj= s3.Object(bucket_name, file_name)
    body =  obj.get()['Body'].read()
    print(body)



aws_access_key_id= "..."
aws_secret_access_key ="..."
region = "..."
bucket_name ="..."

s3 =create_aws_connection(aws_access_key_id, aws_secret_access_key, region)




