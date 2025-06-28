# Social Media Posting Agent with CrewAI

An intelligent agentic system that automatically fetches content from Google Drive and posts to Facebook, Twitter/X, and LinkedIn using CrewAI framework.

## Features

- 🤖 **Multi-Agent System**: Specialized agents for each social media platform
- 📁 **Google Drive Integration**: Automatically fetches content from designated files
- 📱 **Multi-Platform Posting**: Supports Facebook, Twitter/X, and LinkedIn
- ⏰ **Scheduled Posting**: Configurable daily posting schedule
- 🔧 **Configurable**: JSON-based configuration for all credentials and settings
- 📊 **Logging**: Comprehensive logging of all activities

## Architecture

### Agents
- **Content Manager Agent**: Fetches and organizes content from Google Drive
- **Facebook Agent**: Handles Facebook page posting
- **Twitter Agent**: Manages Twitter/X posting with character limit handling
- **LinkedIn Agent**: Posts professional content to LinkedIn
- **Coordinator Agent**: Oversees the entire posting workflow

### Tools
- **Google Drive Tool**: Authenticates and fetches content from Google Drive
- **Facebook Tool**: Posts content using Facebook Graph API
- **Twitter Tool**: Posts tweets using Twitter API v2
- **LinkedIn Tool**: Posts to LinkedIn using LinkedIn API

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Setup Script

```bash
python setup.py
```

This will guide you through:
- Setting up Google Drive API credentials
- Configuring Facebook, Twitter, and LinkedIn API access
- Setting up OpenAI API key
- Configuring content file mapping
- Setting posting schedule

### 3. API Setup Requirements

#### Google Drive API
1. Go to [Google Cloud Console](https://console.developers.google.com/)
2. Create a new project or select existing one
3. Enable Google Drive API
4. Create OAuth 2.0 Client ID credentials
5. Download the credentials JSON file

#### Facebook API
1. Go to [Facebook Developers](https://developers.facebook.com/)
2. Create a new app
3. Add Facebook Login product
4. Get your page access token and page ID

#### Twitter/X API
1. Go to [Twitter Developer Portal](https://developer.twitter.com/)
2. Create a new app
3. Generate API keys, access tokens, and bearer token

#### LinkedIn API
1. Go to [LinkedIn Developers](https://www.linkedin.com/developers/)
2. Create a new app
3. Get authorization and generate access token

#### OpenAI API
1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Create an API key

## Usage

### Running the Scheduler

```bash
# Start the daily scheduler
python scheduler.py

# Test run (execute once)
python scheduler.py --test

# Use custom config file
python scheduler.py --config my_config.json
```

### Manual Execution

```bash
python crew.py
```

## Configuration

The `config.json` file contains all configuration:

```json
{
  "google_drive": {
    "credentials_file": "path/to/google_credentials.json",
    "content_folder_id": "your_google_drive_folder_id",
    "scopes": ["https://www.googleapis.com/auth/drive.readonly"]
  },
  "facebook": {
    "access_token": "your_facebook_access_token",
    "page_id": "your_facebook_page_id"
  },
  "twitter": {
    "api_key": "your_twitter_api_key",
    "api_secret": "your_twitter_api_secret",
    "access_token": "your_twitter_access_token",
    "access_token_secret": "your_twitter_access_token_secret",
    "bearer_token": "your_twitter_bearer_token"
  },
  "linkedin": {
    "access_token": "your_linkedin_access_token",
    "person_id": "your_linkedin_person_id"
  },
  "openai": {
    "api_key": "your_openai_api_key"
  },
  "schedule": {
    "time": "19:00",
    "timezone": "Asia/Kolkata"
  },
  "content_mapping": {
    "facebook": "facebook_content.txt",
    "twitter": "twitter_content.txt",
    "linkedin": "linkedin_content.txt"
  }
}
```

## Content Files Structure

Create separate content files in your Google Drive folder:

- `facebook_content.txt`: Content optimized for Facebook
- `twitter_content.txt`: Content optimized for Twitter (consider 280 char limit)
- `linkedin_content.txt`: Professional content for LinkedIn

## Logging

All activities are logged to:
- Console output
- `social_media_posting.log` file

## Error Handling

The system includes comprehensive error handling for:
- API authentication failures
- Network connectivity issues
- Content fetching errors
- Posting failures
- Rate limiting

## Security Best Practices

- Store API credentials securely
- Use environment variables for sensitive data
- Regularly rotate access tokens
- Monitor API usage and logs
- Keep dependencies updated

## Troubleshooting

### Common Issues

1. **Google Drive Authentication**: Ensure credentials file path is correct and has proper permissions
2. **Social Media API Limits**: Check rate limits and quotas for each platform
3. **Content File Not Found**: Verify file names and Google Drive folder ID
4. **Timezone Issues**: Ensure timezone is correctly specified in config

### Debug Mode

Run with verbose logging:

```bash
python scheduler.py --test
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review logs for error details
3. Ensure all API credentials are valid
4. Verify content files exist in Google Drive

## Roadmap

- [ ] Support for Instagram posting
- [ ] Image and media posting capabilities
- [ ] Content scheduling with different times per platform
- [ ] Analytics and engagement tracking
- [ ] Content optimization suggestions
- [ ] Webhook support for real-time posting
