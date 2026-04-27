# URL Shortener

A small serverless URL shortener built with AWS Lambda, DynamoDB, API Gateway, IAM, and CloudWatch.

Send a long URL to the shorten endpoint and get back a compact short link. When someone opens the short link, API Gateway invokes the redirect Lambda, looks up the original URL in DynamoDB, and redirects the user with an HTTP `301`.

![Architecture diagram](architecture.jpeg)

## What It Does

- Accepts a long URL and returns a short link such as `yourdomain/rv0phj`
- Stores `shortCode -> longUrl` mappings in DynamoDB
- Redirects short-link visitors to the original URL using HTTP `301`
- Tracks a simple click count for each short code
- Logs Lambda invocations through CloudWatch

## Architecture

- **API Gateway** exposes public HTTP endpoints for shortening and redirecting.
- **AWS Lambda** runs two Python functions:
  - `shorten.py` creates a random short code and stores the mapping.
  - `redirect.py` looks up the short code and returns a redirect response.
- **DynamoDB** stores URL mappings using `shortCode` as the lookup key.
- **IAM** grants the Lambda functions only the DynamoDB permissions they need.
- **CloudWatch** captures logs for debugging and observability.

## Access Pattern

The main access pattern is simple and fast:

1. Write a new item by `shortCode` when a URL is shortened.
2. Read an item by `shortCode` when a short link is visited.
3. Update the `clicks` count after a successful lookup.

This keeps the DynamoDB table design focused on the exact queries the application needs.

## API Behavior

### Create a Short URL

Request body:

```json
{
  "longUrl": "https://www.google.com"
}
```

Example response:

```json
{
  "shortCode": "rv0phj",
  "shortUrl": "https://short.ly/rv0phj",
  "longUrl": "https://www.google.com"
}
```

### Redirect

When a user visits:

```text
GET /{shortCode}
```

The redirect Lambda:

1. Reads `{shortCode}` from the path.
2. Looks up the original URL in DynamoDB.
3. Increments the click count.
4. Returns:

```http
HTTP/1.1 301 Moved Permanently
Location: https://original-long-url.com
```

If the short code does not exist, it returns `404`.

## Files

- `shorten.py` - Lambda handler for creating short URLs
- `redirect.py` - Lambda handler for redirecting short URLs
- `dynamo-policy.json` - IAM policy for DynamoDB access
- `test-shorten.json` - sample test payload for the shorten Lambda
- `architecture.jpeg` - project architecture diagram

## What I Learned

- Design access patterns before writing code.
- Build in layers: storage first, code second, expose third.
- Least privilege is not optional; it is the foundation.
- `301` vs `302` is a product decision, not just a technical detail.

