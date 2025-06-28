# Facebook API Authentication & Setup Guide

This guide provides detailed step-by-step instructions for setting up Facebook API access for automated posting to your Facebook page.

## Prerequisites

- A Facebook account
- A Facebook page (not personal profile) where you want to post
- Admin access to the Facebook page

## Step 1: Create a Facebook Developer Account

1. **Go to Facebook Developers**
   - Visit [https://developers.facebook.com/](https://developers.facebook.com/)
   - Click "Get Started" in the top right corner

2. **Register as a Developer**
   - Log in with your Facebook account
   - Accept the Facebook Developer Terms and Policies
   - Verify your account via email or phone if prompted

3. **Complete Developer Registration**
   - Provide your contact information
   - Choose your primary use case (select "Other" if unsure)
   - Complete the registration process

## Step 2: Create a Facebook App

1. **Create New App**
   - From the Facebook Developers dashboard, click "Create App"
   - Choose "Business" as the app type
   - Click "Next"

2. **App Details**
   - **Display Name**: Enter a name for your app (e.g., "Social Media Posting Bot")
   - **App Contact Email**: Use your email address
   - **Business Account**: Select your business account or create one
   - Click "Create App"

3. **App Dashboard**
   - You'll be redirected to your app dashboard
   - Note down your **App ID** (you'll need this later)

## Step 3: Add Facebook Login Product

1. **Add Product**
   - In your app dashboard, scroll down to "Add Products to Your App"
   - Find "Facebook Login" and click "Set Up"

2. **Configure Facebook Login**
   - In the left sidebar, click "Facebook Login" → "Settings"
   - Under "Valid OAuth Redirect URIs", add:
     ```
     https://localhost/
     http://localhost/
     ```
   - Click "Save Changes"

## Step 4: Configure App Settings

1. **Basic Settings**
   - Go to "Settings" → "Basic" in the left sidebar
   - Fill in required fields:
     - **Privacy Policy URL**: Add your privacy policy URL (required for public apps)
     - **Terms of Service URL**: Add your terms of service URL (optional)
     - **App Category**: Choose appropriate category

2. **App Review**
   - For testing purposes, your app starts in "Development Mode"
   - You can test with accounts that have roles in your app
   - For production use, you'll need to submit for App Review

## Step 5: Get Page Access Token

### Method 1: Using Graph API Explorer (Recommended for Testing)

1. **Access Graph API Explorer**
   - Go to [https://developers.facebook.com/tools/explorer/](https://developers.facebook.com/tools/explorer/)
   - Select your app from the dropdown

2. **Generate User Access Token**
   - Click "Generate Access Token"
   - Log in and grant permissions
   - Select the following permissions:
     - `pages_manage_posts`
     - `pages_read_engagement`
     - `pages_show_list`
   - Click "Generate Access Token"

3. **Get Page Access Token**
   - In the Graph API Explorer, make a GET request to:
     ```
     /me/accounts
     ```
   - This will return a list of pages you manage
   - Find your target page and copy its `access_token`
   - Also note the `id` (this is your Page ID)

### Method 2: Using Facebook Business Manager (For Production)

1. **Create System User**
   - Go to [Facebook Business Manager](https://business.facebook.com/)
   - Navigate to "Business Settings" → "Users" → "System Users"
   - Click "Add" to create a new system user
   - Give it a name and assign "Admin" role

2. **Generate Access Token**
   - Click on your system user
   - Click "Generate New Token"
   - Select your app
   - Choose permissions:
     - `pages_manage_posts`
     - `pages_read_engagement`
     - `pages_show_list`
   - Set token expiration (choose "Never" for long-term use)
   - Generate and copy the token

3. **Assign Page Access**
   - Go to "Business Settings" → "Accounts" → "Pages"
   - Select your page
   - Click "Assign Partner"
   - Add your app and grant necessary permissions

## Step 6: Get Your Page ID

### Method 1: From Graph API Explorer
- Use the `/me/accounts` endpoint as described above

### Method 2: From Facebook Page
1. Go to your Facebook page
2. Click "About" in the left sidebar
3. Scroll down to find "Page ID" or "Facebook Page ID"

### Method 3: From Page URL
- If your page URL is `https://www.facebook.com/YourPageName`
- Go to `https://www.facebook.com/YourPageName/about`
- Look for the Page ID in the page information

## Step 7: Test Your Setup

1. **Test API Call**
   - Use Graph API Explorer or a tool like Postman
   - Make a POST request to:
     ```
     https://graph.facebook.com/v18.0/{PAGE_ID}/feed
     ```
   - Headers:
     ```
     Content-Type: application/json
     ```
   - Body:
     ```json
     {
       "message": "Test post from API",
       "access_token": "YOUR_PAGE_ACCESS_TOKEN"
     }
     ```

2. **Verify Post**
   - Check your Facebook page to see if the test post appeared
   - If successful, you're ready to use the API

## Step 8: Configure Your Application

Add the following to your `config.json`:

```json
{
  "facebook": {
    "access_token": "YOUR_PAGE_ACCESS_TOKEN",
    "page_id": "YOUR_PAGE_ID"
  }
}
```

## Important Security Notes

### Token Security
- **Never commit access tokens to version control**
- Store tokens securely (environment variables, secure config files)
- Regularly rotate access tokens
- Use the minimum required permissions

### Token Expiration
- User access tokens expire in 1-2 hours
- Page access tokens can be long-lived (60 days) or permanent
- System user tokens can be set to never expire
- Monitor token expiration and implement refresh logic

### Rate Limits
- Facebook has rate limits for API calls
- Standard limit: 200 calls per hour per user
- Page-level limits may apply
- Implement proper error handling for rate limit responses

## Troubleshooting

### Common Issues

1. **"Invalid OAuth access token" Error**
   - Token may have expired
   - Regenerate the access token
   - Ensure you're using the page access token, not user token

2. **"Insufficient permissions" Error**
   - Check that your app has the required permissions
   - Ensure the page access token includes `pages_manage_posts`
   - Verify the user has admin access to the page

3. **"App not approved" Error**
   - For production use, submit your app for review
   - For testing, ensure test users have appropriate roles

4. **Page not found**
   - Verify the Page ID is correct
   - Ensure the access token has access to the specific page

### Testing Checklist

- [ ] App created and configured
- [ ] Facebook Login product added
- [ ] Required permissions granted
- [ ] Page access token generated
- [ ] Page ID obtained
- [ ] Test post successful
- [ ] Tokens stored securely

## API Reference

### Useful Endpoints

- **Get Pages**: `GET /me/accounts`
- **Post to Page**: `POST /{page-id}/feed`
- **Get Page Info**: `GET /{page-id}`
- **Get Page Posts**: `GET /{page-id}/posts`

### Required Permissions

- `pages_manage_posts`: Post to pages
- `pages_read_engagement`: Read page insights
- `pages_show_list`: List pages user manages

## Production Considerations

### App Review Process
1. **Submit for Review**
   - Required for public apps
   - Provide detailed use case description
   - Include privacy policy and terms of service

2. **Business Verification**
   - May be required for certain permissions
   - Provide business documentation

### Monitoring
- Set up logging for API calls
- Monitor rate limits and usage
- Implement error handling and retry logic
- Track token expiration dates

### Compliance
- Follow Facebook Platform Policies
- Respect user privacy and data protection laws
- Implement proper content moderation if needed

## Support Resources

- [Facebook Developers Documentation](https://developers.facebook.com/docs/)
- [Graph API Reference](https://developers.facebook.com/docs/graph-api/)
- [Facebook Platform Policies](https://developers.facebook.com/policy/)
- [Facebook Developer Community](https://developers.facebook.com/community/)

---

**Note**: Facebook's API and policies change frequently. Always refer to the official Facebook Developers documentation for the most up-to-date information.
