"""
Send info to bucket
"""
import os
import boto3

def upload_files(path):
    '''Upload files to AWS Bucket'''
    # session = boto3.Session(
    #     aws_access_key_id='xx',
    #     aws_secret_access_key='xx',
    #     region_name='us-east-1'
    # )
    # client = boto3.client(
    #     's3',
    #     aws_access_key_id='xx',
    #     aws_secret_access_key='xx',
    #     region_name='us-east-1'
    # )
    session = boto3.Session(profile_name='default')
    # s3 = client.resource('s3') #session.resource('s3')
    session = session.resource('s3')
    bucket = session.Bucket('enigmaco-data')
    for subdir, _, files in os.walk(path):
        for file in files:
            full_path = os.path.join(subdir, file)
            with open(full_path, 'rb') as data:
                key = full_path[len(path)+1:].replace('\\', '/')
                print('Uploading: {} to {}'.format(full_path, key))
                # s3.Object('enigmaco-data', key).put(Body=data)
                # client.put_object(ACL='public-read', Bucket='enigmaco-data', Body=data, Key=key)
                bucket.put_object(ACL='public-read', Body=data, Key=key)
                # print(client.delete_object(Bucket='enigmaco-data', Key=key))

upload_files('repository')
