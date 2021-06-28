import boto3
import os
import sys
import json


class Queue:
    def __init__(self, region_name, aws_access_key_id, aws_secret_access_key, QueueName):
        self.sqs = boto3.resource('sqs', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region_name)
        self.QueueName = QueueName


    def send_message(self, filename, BucketName):
        ## check that queue exists
        try:
            queue = self.sqs.get_queue_by_name(QueueName=self.QueueName)
        except KeyError:
            sys.stdout.write(f'{self.QueueName} cannot be found. \n')

        ## filename and BucketName are added to queue
        ## note: relevant info are stored as message attributes, not message body!
        response = queue.send_message(MessageBody='test', MessageAttributes={
            'filename': {
                'DataType': 'String',
                'StringValue': filename,
            },
            'BucketName': {
                'DataType': 'String',
                'StringValue': BucketName,
            },
        })
        sys.stdout.write(f'{filename} has been added to queue. \n')


    def receive_message(self):
        ## check that queue exists
        try:
            queue = self.sqs.get_queue_by_name(QueueName=self.QueueName)
        except KeyError:
            sys.stdout.write(f'{self.QueueName} cannot be found. \n')

        response = queue.receive_messages(
            MessageAttributeNames=['filename', 'BucketName'], 
            MaxNumberOfMessages=1, 
            WaitTimeSeconds=10,
            )

        if response:
            ## there should be only 1 message in response
            for msg in response:
                info = json.dumps({
                    'filename':msg.message_attributes.get('filename').get('StringValue'), 
                    'BucketName':msg.message_attributes.get('BucketName').get('StringValue')})
        

