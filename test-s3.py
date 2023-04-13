import boto3 

# Upload
'''
s3_client = boto3.client('s3')
# response = s3_client.upload_file(file_name, bucket, object_name)
response = s3_client.upload_file('RamiBruce.jpg', 'aicore-rr', 'ScottishKing.jpg')
'''

# View
'''
s3 = boto3.resource('s3')
my_bucket = s3.Bucket('aicore-rr')
for file in my_bucket.objects.all():
    print(file.key)
'''

# Download
'''
s3 = boto3.client('s3')
# Ofcourse, change the names of the files to match yours.
s3.download_file('aicore-rr', 'ScottishKing.jpg', 'FunnyRami.jpg')
'''

# Another download after making bucket public
import requests
# Change this with your URL
url = 'https://aicore-rr.s3.eu-west-2.amazonaws.com/ScottishKing.jpg'
response = requests.get(url)
with open('ScottishKing.jpg', 'wb') as f:
    f.write(response.content)
