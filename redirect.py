import json
import boto3

# This connects to DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-1')
table = dynamodb.Table('url-shortener')

def handler(event, context):
    try:
        # Step 1 — Get the short code from the URL
        # e.g. user visits /aB3xZ9 → short_code = "aB3xZ9"
        short_code = event['pathParameters']['shortCode']

        # Step 2 — Look it up in DynamoDB
        response = table.get_item(Key={'shortCode': short_code})

        # Step 3 — If not found, return 404
        if 'Item' not in response:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'Short URL not found'})
            }

        # Step 4 — Get the original long URL
        long_url = response['Item']['longUrl']

        # Step 5 — Update click count
        table.update_item(
            Key={'shortCode': short_code},
            UpdateExpression='SET clicks = clicks + :val',
            ExpressionAttributeValues={':val': 1}
        )

        # Step 6 — Redirect the user
        return {
            'statusCode': 301,
            'headers': {'Location': long_url},
            'body': ''
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }