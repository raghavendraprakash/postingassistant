# Twitter/X API Authentication & Setup Guide

This guide provides comprehensive step-by-step instructions for setting up Twitter/X API access for automated posting to your Twitter/X account.

## Prerequisites

- A Twitter/X account
- A valid phone number associated with your Twitter/X account
- Email verification completed on your Twitter/X account

## Step 1: Apply for Twitter Developer Account

1. **Visit Twitter Developer Portal**
   - Go to [https://developer.twitter.com/](https://developer.twitter.com/)
   - Click "Apply" in the top right corner

2. **Sign in to Twitter**
   - Log in with your Twitter/X account credentials
   - Ensure your account is in good standing

3. **Choose Account Type**
   - Select "Hobbyist" for personal projects
   - Select "Professional" for business use
   - Click "Get Started"

4. **Specify Use Case**
   - Choose the most appropriate option:
     - "Making a bot" (for automated posting)
     - "Academic research"
     - "Personal use"
   - Click "Next"

5. **Provide Application Details**
   - **Country**: Select your country
   - **Coding Experience**: Choose your level
   - **Use Case Description**: Provide detailed explanation (200+ words)
     ```
     Example:
     I am developing a social media automation tool for personal use to 
     schedule and post content across multiple platforms. The application 
     will read content from Google Drive and post to Twitter/X, Facebook, 
     and LinkedIn. This tool will help maintain consistent social media 
     presence by automating the posting process. The content will be 
     original and comply with Twitter's terms of service.
     ```

6. **Review and Submit**
   - Review your application
   - Accept the Developer Agreement and Policy
   - Click "Submit Application"

7. **Email Verification**
   - Check your email for verification link
   - Click the verification link to confirm your application

## Step 2: Wait for Approval

- **Processing Time**: Usually 1-7 days
- **Status Check**: Monitor your email and developer portal
- **Follow-up**: Twitter may request additional information

## Step 3: Create a Twitter App

1. **Access Developer Dashboard**
   - Once approved, go to [https://developer.twitter.com/en/portal/dashboard](https://developer.twitter.com/en/portal/dashboard)
   - Click "Create App" or "New Project"

2. **Create Project (New Interface)**
   - **Project Name**: Enter a descriptive name (e.g., "Social Media Automation")
   - **Use Case**: Select appropriate use case
   - **Project Description**: Provide detailed description
   - Click "Next"

3. **Create App within Project**
   - **App Name**: Enter unique app name (e.g., "SocialMediaBot")
   - **App Description**: Describe your app's functionality
   - Click "Complete"

## Step 4: Configure App Settings

1. **App Settings**
   - Navigate to your app in the developer dashboard
   - Click on "Settings" tab

2. **App Permissions**
   - Click "Set up" under "User authentication settings"
   - **App Permissions**: Select "Read and Write" (required for posting)
   - **Type of App**: Choose "Web App, Automated App or Bot"
   - **App Info**:
     - **Callback URI**: `https://localhost:3000/callback`
     - **Website URL**: Your website or `https://example.com`
     - **Terms of Service**: Your terms URL (optional)
     - **Privacy Policy**: Your privacy policy URL (optional)
   - Click "Save"

## Step 5: Generate API Keys and Tokens

### API Keys and Secrets

1. **Navigate to Keys and Tokens**
   - In your app dashboard, click "Keys and Tokens" tab

2. **API Key and Secret**
   - Under "Consumer Keys", you'll see:
     - **API Key** (Consumer Key)
     - **API Key Secret** (Consumer Secret)
   - Click "Regenerate" if you need new keys
   - **Important**: Copy and store these securely

### Access Tokens

1. **Generate Access Token and Secret**
   - Under "Access Token and Secret" section
   - Click "Generate" button
   - Copy both:
     - **Access Token**
     - **Access Token Secret**
   - **Important**: Store these securely

### Bearer Token

1. **Bearer Token**
   - Under "Bearer Token" section
   - Click "Generate" if not already generated
   - Copy the **Bearer Token**
   - This is used for API v2 endpoints

## Step 6: API Version Selection

### Twitter API v1.1 vs v2

**For Posting Tweets (Our Use Case):**
- **API v1.1**: Use `POST statuses/update` endpoint
- **API v2**: Use `POST /2/tweets` endpoint (recommended)

**Authentication Methods:**
- **OAuth 1.0a**: Uses API Key, API Secret, Access Token, Access Token Secret
- **OAuth 2.0**: Uses Bearer Token (read-only operations)
- **For Posting**: Use OAuth 1.0a with all four credentials

## Step 7: Test Your Setup

### Using Python (Tweepy)

1. **Install Tweepy**
   ```bash
   pip install tweepy
   ```

2. **Test Script**
   ```python
   import tweepy
   
   # API v2 Client
   client = tweepy.Client(
       bearer_token="YOUR_BEARER_TOKEN",
       consumer_key="YOUR_API_KEY",
       consumer_secret="YOUR_API_SECRET",
       access_token="YOUR_ACCESS_TOKEN",
       access_token_secret="YOUR_ACCESS_TOKEN_SECRET",
       wait_on_rate_limit=True
   )
   
   # Test tweet
   try:
       response = client.create_tweet(text="Hello World! Testing Twitter API")
       print(f"Tweet posted successfully: {response.data['id']}")
   except Exception as e:
       print(f"Error: {e}")
   ```

### Using cURL

```bash
curl -X POST "https://api.twitter.com/2/tweets" \
  -H "Authorization: Bearer YOUR_BEARER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello World from API!"}'
```

## Step 8: Configure Your Application

Add the following to your `config.json`:

```json
{
  "twitter": {
    "api_key": "YOUR_API_KEY",
    "api_secret": "YOUR_API_SECRET",
    "access_token": "YOUR_ACCESS_TOKEN",
    "access_token_secret": "YOUR_ACCESS_TOKEN_SECRET",
    "bearer_token": "YOUR_BEARER_TOKEN"
  }
}
```

## Rate Limits and Quotas

### API v2 Rate Limits (Per 15-minute window)

**Free Tier:**
- **Tweet Creation**: 300 requests per 15 minutes
- **Tweet Lookup**: 75 requests per 15 minutes
- **User Lookup**: 75 requests per 15 minutes

**Basic Tier ($100/month):**
- **Tweet Creation**: 300 requests per 15 minutes
- **Tweet Lookup**: 10,000 requests per 15 minutes
- **User Lookup**: 10,000 requests per 15 minutes

### Monthly Usage Limits

**Free Tier:**
- **Tweet Creation**: 1,500 tweets per month
- **Tweet Reads**: 10,000 tweets per month

## Content Guidelines and Best Practices

### Tweet Content Rules
- **Character Limit**: 280 characters
- **Media**: Images, videos, GIFs allowed
- **Links**: URLs count toward character limit
- **Hashtags**: Use relevant hashtags (recommended 1-2 per tweet)

### Automation Best Practices
- **Avoid Spam**: Don't post identical content repeatedly
- **Rate Limiting**: Respect API rate limits
- **Content Quality**: Post valuable, original content
- **Engagement**: Mix automated posts with manual engagement

### Prohibited Content
- Spam or misleading information
- Harassment or abusive content
- Copyright infringement
- Adult content (without proper labeling)

## Error Handling

### Common Error Codes

- **401 Unauthorized**: Invalid credentials or expired tokens
- **403 Forbidden**: Insufficient permissions or suspended account
- **429 Too Many Requests**: Rate limit exceeded
- **400 Bad Request**: Invalid request format or parameters

### Error Response Example
```json
{
  "errors": [
    {
      "code": 187,
      "message": "Status is a duplicate."
    }
  ]
}
```

## Security Best Practices

### Credential Security
- **Never expose API keys** in public repositories
- **Use environment variables** for sensitive data
- **Rotate keys regularly** (every 90 days recommended)
- **Monitor usage** in developer dashboard

### Token Management
- **Store securely**: Use encrypted storage or secure vaults
- **Limit scope**: Use minimum required permissions
- **Monitor access**: Check for unusual API usage patterns

## Troubleshooting

### Common Issues

1. **"Could not authenticate you" Error**
   - Verify all four credentials are correct
   - Check if tokens have expired
   - Ensure proper OAuth signature generation

2. **"Your account is suspended" Error**
   - Check account status in Twitter
   - Review recent activity for policy violations
   - Contact Twitter support if needed

3. **"Rate limit exceeded" Error**
   - Implement proper rate limiting in your code
   - Use `wait_on_rate_limit=True` in Tweepy
   - Monitor usage in developer dashboard

4. **"Duplicate status" Error**
   - Twitter prevents posting identical tweets
   - Add timestamp or unique identifier to content
   - Check recent tweets before posting

### Testing Checklist

- [ ] Developer account approved
- [ ] App created and configured
- [ ] Read and Write permissions enabled
- [ ] All API keys and tokens generated
- [ ] Test tweet posted successfully
- [ ] Rate limiting implemented
- [ ] Error handling in place

## Advanced Features

### Media Upload
```python
# Upload image with tweet
media = api.media_upload("image.jpg")
client.create_tweet(text="Tweet with image", media_ids=[media.media_id])
```

### Thread Creation
```python
# Create tweet thread
tweet1 = client.create_tweet(text="First tweet in thread")
tweet2 = client.create_tweet(
    text="Second tweet in thread", 
    in_reply_to_tweet_id=tweet1.data['id']
)
```

### Scheduled Tweets
- Twitter API doesn't support native scheduling
- Implement scheduling in your application
- Use cron jobs or task schedulers

## Monitoring and Analytics

### Usage Monitoring
- Check developer dashboard regularly
- Monitor rate limit usage
- Track API response times

### Analytics
- Use Twitter Analytics for engagement metrics
- Monitor tweet performance
- Adjust posting strategy based on data

## Migration from API v1.1 to v2

### Key Differences
- **Endpoints**: Different URL structure
- **Authentication**: Bearer token for read operations
- **Response Format**: JSON structure changes
- **Features**: New features in v2 (polls, spaces, etc.)

### Migration Steps
1. Update authentication method
2. Change endpoint URLs
3. Modify request/response handling
4. Test thoroughly before production

## Support Resources

- [Twitter Developer Documentation](https://developer.twitter.com/en/docs)
- [API Reference](https://developer.twitter.com/en/docs/api-reference-index)
- [Tweepy Documentation](https://docs.tweepy.org/)
- [Twitter Developer Community](https://twittercommunity.com/)
- [Status Page](https://api.twitterstat.us/)

## Pricing Information

### Free Tier
- 1,500 tweets per month
- 50,000 tweet reads per month
- Basic support

### Basic Tier ($100/month)
- 3,000 tweets per month
- 10,000 tweet reads per month
- Email support

### Pro Tier ($5,000/month)
- 300,000 tweets per month
- 1,000,000 tweet reads per month
- Priority support

---

**Note**: Twitter/X API policies and pricing change frequently. Always refer to the official Twitter Developer documentation for the most current information.
