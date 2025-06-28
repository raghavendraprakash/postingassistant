# LinkedIn API Authentication & Setup Guide

This guide provides comprehensive step-by-step instructions for setting up LinkedIn API access for automated posting to your LinkedIn profile or company page.

## Prerequisites

- A LinkedIn account (personal or business)
- Verified email address on LinkedIn
- Complete LinkedIn profile
- For company posting: Admin access to LinkedIn company page

## Step 1: Create LinkedIn Developer Account

1. **Visit LinkedIn Developers**
   - Go to [https://www.linkedin.com/developers/](https://www.linkedin.com/developers/)
   - Click "Join the LinkedIn Developer Program"

2. **Sign in to LinkedIn**
   - Log in with your LinkedIn credentials
   - Ensure your profile is complete and professional

3. **Accept Developer Agreement**
   - Read and accept the LinkedIn API Terms of Use
   - Complete the developer registration process

## Step 2: Create a LinkedIn App

1. **Create New App**
   - From the LinkedIn Developers dashboard, click "Create App"
   - You'll need to provide app details

2. **App Information**
   - **App Name**: Enter a descriptive name (e.g., "Social Media Automation Tool")
   - **LinkedIn Page**: 
     - For personal posting: Select your personal LinkedIn page
     - For company posting: Select your company page (you must be admin)
   - **Privacy Policy URL**: Provide a valid privacy policy URL
   - **App Logo**: Upload a logo (recommended 300x300px)
   - **Legal Agreement**: Accept the terms

3. **Submit for Review**
   - Click "Create App"
   - Your app will be created but may need verification

## Step 3: Configure App Products

### Request Access to Products

1. **Navigate to Products Tab**
   - In your app dashboard, click on "Products" tab
   - You'll see available products to request

2. **Sign In with LinkedIn using OpenID Connect**
   - Click "Request Access"
   - This provides basic profile access
   - Usually auto-approved

3. **Share on LinkedIn**
   - Click "Request Access" 
   - Required for posting content
   - May require review process

4. **Marketing Developer Platform** (Optional)
   - For advanced marketing features
   - Requires business verification

### Product Approval Process
- **Automatic Approval**: Basic products (Sign In with LinkedIn)
- **Review Required**: Share on LinkedIn, Marketing features
- **Review Time**: 7-14 business days typically

## Step 4: Configure OAuth Settings

1. **Auth Tab Configuration**
   - Click on "Auth" tab in your app dashboard
   - Configure OAuth 2.0 settings

2. **OAuth 2.0 Settings**
   - **Authorized Redirect URLs**: Add your callback URLs
     ```
     https://localhost:3000/callback
     https://your-domain.com/auth/linkedin/callback
     ```
   - **Client ID**: Note this down (you'll need it)
   - **Client Secret**: Generate and securely store this

3. **OAuth 2.0 Scopes**
   - Based on approved products, you'll have access to scopes:
     - `r_liteprofile`: Basic profile info
     - `r_emailaddress`: Email address
     - `w_member_social`: Post on behalf of user

## Step 5: Authentication Flow

### OAuth 2.0 Authorization Code Flow

1. **Authorization URL**
   ```
   https://www.linkedin.com/oauth/v2/authorization?
   response_type=code&
   client_id=YOUR_CLIENT_ID&
   redirect_uri=YOUR_REDIRECT_URI&
   state=RANDOM_STRING&
   scope=r_liteprofile%20r_emailaddress%20w_member_social
   ```

2. **Get Authorization Code**
   - User visits authorization URL
   - Grants permissions
   - LinkedIn redirects to your callback with authorization code

3. **Exchange Code for Access Token**
   ```bash
   curl -X POST https://www.linkedin.com/oauth/v2/accessToken \
     -H 'Content-Type: application/x-www-form-urlencoded' \
     -d 'grant_type=authorization_code' \
     -d 'code=AUTHORIZATION_CODE' \
     -d 'client_id=YOUR_CLIENT_ID' \
     -d 'client_secret=YOUR_CLIENT_SECRET' \
     -d 'redirect_uri=YOUR_REDIRECT_URI'
   ```

4. **Access Token Response**
   ```json
   {
     "access_token": "ACCESS_TOKEN",
     "expires_in": 5184000,
     "refresh_token": "REFRESH_TOKEN",
     "refresh_token_expires_in": 31536000,
     "scope": "r_liteprofile,r_emailaddress,w_member_social"
   }
   ```

## Step 6: Get User/Person ID

### Get Current User Profile

```bash
curl -X GET https://api.linkedin.com/v2/people/~?projection=(id,firstName,lastName) \
  -H 'Authorization: Bearer YOUR_ACCESS_TOKEN'
```

**Response:**
```json
{
  "id": "PERSON_ID",
  "firstName": {
    "localized": {
      "en_US": "John"
    }
  },
  "lastName": {
    "localized": {
      "en_US": "Doe"
    }
  }
}
```

**Note the `id` field - this is your Person ID needed for posting.**

## Step 7: Test Posting

### Create a Text Post

```bash
curl -X POST https://api.linkedin.com/v2/ugcPosts \
  -H 'Authorization: Bearer YOUR_ACCESS_TOKEN' \
  -H 'Content-Type: application/json' \
  -H 'X-Restli-Protocol-Version: 2.0.0' \
  -d '{
    "author": "urn:li:person:PERSON_ID",
    "lifecycleState": "PUBLISHED",
    "specificContent": {
      "com.linkedin.ugc.ShareContent": {
        "shareCommentary": {
          "text": "Hello LinkedIn! Testing API integration."
        },
        "shareMediaCategory": "NONE"
      }
    },
    "visibility": {
      "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
    }
  }'
```

### Python Example

```python
import requests
import json

def post_to_linkedin(access_token, person_id, content):
    url = "https://api.linkedin.com/v2/ugcPosts"
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'X-Restli-Protocol-Version': '2.0.0'
    }
    
    post_data = {
        "author": f"urn:li:person:{person_id}",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": content
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }
    
    response = requests.post(url, headers=headers, json=post_data)
    return response.json()

# Usage
result = post_to_linkedin(
    access_token="YOUR_ACCESS_TOKEN",
    person_id="YOUR_PERSON_ID",
    content="Hello from Python!"
)
print(result)
```

## Step 8: Configure Your Application

Add the following to your `config.json`:

```json
{
  "linkedin": {
    "access_token": "YOUR_ACCESS_TOKEN",
    "person_id": "YOUR_PERSON_ID"
  }
}
```

## Advanced Posting Features

### Post with Media

1. **Upload Media First**
   ```bash
   curl -X POST https://api.linkedin.com/v2/assets?action=registerUpload \
     -H 'Authorization: Bearer YOUR_ACCESS_TOKEN' \
     -H 'Content-Type: application/json' \
     -d '{
       "registerUploadRequest": {
         "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
         "owner": "urn:li:person:PERSON_ID",
         "serviceRelationships": [{
           "relationshipType": "OWNER",
           "identifier": "urn:li:userGeneratedContent"
         }]
       }
     }'
   ```

2. **Upload Image Binary**
   ```bash
   curl -X PUT "UPLOAD_URL_FROM_PREVIOUS_RESPONSE" \
     -H 'Authorization: Bearer YOUR_ACCESS_TOKEN' \
     --data-binary @image.jpg
   ```

3. **Create Post with Media**
   ```json
   {
     "author": "urn:li:person:PERSON_ID",
     "lifecycleState": "PUBLISHED",
     "specificContent": {
       "com.linkedin.ugc.ShareContent": {
         "shareCommentary": {
           "text": "Check out this image!"
         },
         "shareMediaCategory": "IMAGE",
         "media": [{
           "status": "READY",
           "description": {
             "text": "Image description"
           },
           "media": "ASSET_URN_FROM_UPLOAD",
           "title": {
             "text": "Image Title"
           }
         }]
       }
     },
     "visibility": {
       "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
     }
   }
   ```

### Post with Link Preview

```json
{
  "author": "urn:li:person:PERSON_ID",
  "lifecycleState": "PUBLISHED",
  "specificContent": {
    "com.linkedin.ugc.ShareContent": {
      "shareCommentary": {
        "text": "Check out this interesting article!"
      },
      "shareMediaCategory": "ARTICLE",
      "media": [{
        "status": "READY",
        "description": {
          "text": "Article description"
        },
        "originalUrl": "https://example.com/article",
        "title": {
          "text": "Article Title"
        }
      }]
    }
  },
  "visibility": {
    "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
  }
}
```

## Rate Limits and Quotas

### API Rate Limits

**Personal Posts:**
- **UGC Posts**: 100 requests per day per person
- **Profile API**: 500 requests per day per app

**Company Posts:**
- **Organization Posts**: 100 requests per day per organization
- **Company API**: 500 requests per day per app

### Throttling
- LinkedIn implements intelligent throttling
- Respect HTTP 429 responses
- Implement exponential backoff

## Token Management

### Access Token Lifecycle
- **Expires**: 60 days by default
- **Refresh Token**: 365 days
- **Scope**: Limited to approved permissions

### Token Refresh
```bash
curl -X POST https://www.linkedin.com/oauth/v2/accessToken \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=refresh_token' \
  -d 'refresh_token=YOUR_REFRESH_TOKEN' \
  -d 'client_id=YOUR_CLIENT_ID' \
  -d 'client_secret=YOUR_CLIENT_SECRET'
```

## Company Page Posting

### Additional Setup for Company Pages

1. **Company Page Admin Access**
   - Must be admin of the LinkedIn company page
   - Verify admin status in LinkedIn

2. **Get Organization ID**
   ```bash
   curl -X GET https://api.linkedin.com/v2/organizationAcls?q=roleAssignee \
     -H 'Authorization: Bearer YOUR_ACCESS_TOKEN'
   ```

3. **Post to Company Page**
   ```json
   {
     "author": "urn:li:organization:ORGANIZATION_ID",
     "lifecycleState": "PUBLISHED",
     "specificContent": {
       "com.linkedin.ugc.ShareContent": {
         "shareCommentary": {
           "text": "Company update from API"
         },
         "shareMediaCategory": "NONE"
       }
     },
     "visibility": {
       "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
     }
   }
   ```

## Content Guidelines

### Best Practices
- **Professional Tone**: Maintain professional language
- **Value-Driven**: Share insights, tips, industry news
- **Engagement**: Ask questions, encourage discussion
- **Hashtags**: Use 3-5 relevant hashtags
- **Length**: Optimal post length 150-300 characters

### Content Types That Perform Well
- Industry insights and trends
- Professional achievements
- Educational content
- Behind-the-scenes content
- Thought leadership articles

## Error Handling

### Common Error Codes

- **401 Unauthorized**: Invalid or expired access token
- **403 Forbidden**: Insufficient permissions
- **422 Unprocessable Entity**: Invalid request data
- **429 Too Many Requests**: Rate limit exceeded

### Error Response Example
```json
{
  "errorCode": 0,
  "message": "Access token does not have permission to post on behalf of this member",
  "requestId": "REQUEST_ID",
  "status": 403,
  "timestamp": 1234567890
}
```

## Security Best Practices

### Credential Security
- **Store securely**: Use environment variables or secure vaults
- **Never expose**: Don't commit tokens to version control
- **Rotate regularly**: Refresh tokens before expiration
- **Monitor usage**: Check for unusual API activity

### OAuth Security
- **State parameter**: Use random state to prevent CSRF
- **HTTPS only**: Always use HTTPS for redirects
- **Validate tokens**: Verify token scope and expiration

## Troubleshooting

### Common Issues

1. **"Invalid access token" Error**
   - Check token expiration
   - Verify token scope includes required permissions
   - Ensure proper Bearer token format

2. **"Insufficient permissions" Error**
   - Verify app has "Share on LinkedIn" product approved
   - Check OAuth scope includes `w_member_social`
   - Confirm user granted necessary permissions

3. **"Member does not have permission to post" Error**
   - Verify person ID is correct
   - Check if account has posting restrictions
   - Ensure user completed LinkedIn profile

4. **Rate limit exceeded**
   - Implement proper rate limiting
   - Use exponential backoff for retries
   - Monitor daily quota usage

### Testing Checklist

- [ ] LinkedIn Developer account created
- [ ] App created and configured
- [ ] "Share on LinkedIn" product approved
- [ ] OAuth settings configured
- [ ] Access token obtained
- [ ] Person ID retrieved
- [ ] Test post successful
- [ ] Error handling implemented

## Monitoring and Analytics

### Usage Monitoring
- Track API calls in developer dashboard
- Monitor rate limit usage
- Log successful/failed requests

### Content Performance
- Use LinkedIn Analytics for engagement metrics
- Track post reach and impressions
- Analyze best performing content types

## Migration and Updates

### API Versioning
- LinkedIn uses versioned APIs
- Current version: v2
- Monitor deprecation notices

### Staying Updated
- Subscribe to LinkedIn Developer updates
- Follow LinkedIn Engineering blog
- Join LinkedIn Developer community

## Support Resources

- [LinkedIn Developer Documentation](https://docs.microsoft.com/en-us/linkedin/)
- [API Reference](https://docs.microsoft.com/en-us/linkedin/shared/api-guide)
- [LinkedIn Developer Support](https://www.linkedin.com/help/linkedin/answer/a1342443)
- [LinkedIn Engineering Blog](https://engineering.linkedin.com/)
- [Developer Community](https://www.linkedin.com/groups/25827/)

## Compliance and Policies

### LinkedIn API Policy
- Respect user privacy and data
- Don't spam or post irrelevant content
- Follow professional networking guidelines
- Comply with data protection regulations

### Content Policies
- No misleading or false information
- Respect intellectual property rights
- Professional and appropriate content only
- No automated engagement (likes, comments)

---

**Note**: LinkedIn API policies and features evolve regularly. Always refer to the official LinkedIn Developer documentation for the most current information and best practices.
