import json
import boto3
import string
import random
from datetime import datetime

# This connects to DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-1')
table = dynamodb.Table('url-shortener')

def generate_short_code():
    # Creates a random 6 character code like "aB3xZ9"
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=6))

def handler(event, context):
    try:
        # Step 1 — Read the long URL the user sent
        body = json.loads(event['body'])
        long_url = body['longUrl']

        # Step 2 — Generate a short code
        short_code = generate_short_code()

        # Step 3 — Save to DynamoDB
        table.put_item(Item={
            'shortCode': short_code,
            'longUrl':   long_url,
            'createdAt': datetime.utcnow().isoformat(),
            'clicks':    0
        })

        # Step 4 — Return the short URL
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'shortCode': short_code,
                'shortUrl':  f'https://short.ly/{short_code}',
                'longUrl':   long_url
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }