import json
import os
from google_auth_oauthlib.flow import InstalledAppFlow


def setup_google_drive():
    """Setup Google Drive API credentials"""
    print("🔧 Setting up Google Drive API...")
    print("1. Go to https://console.developers.google.com/")
    print("2. Create a new project or select existing one")
    print("3. Enable Google Drive API")
    print("4. Create credentials (OAuth 2.0 Client ID)")
    print("5. Download the credentials JSON file")
    
    credentials_path = input("Enter path to your Google Drive credentials JSON file: ")
    
    if os.path.exists(credentials_path):
        print("✅ Google Drive credentials file found")
        return credentials_path
    else:
        print("❌ Credentials file not found")
        return None


def setup_facebook():
    """Setup Facebook API credentials"""
    print("\n🔧 Setting up Facebook API...")
    print("1. Go to https://developers.facebook.com/")
    print("2. Create a new app")
    print("3. Add Facebook Login product")
    print("4. Get your access token and page ID")
    
    access_token = input("Enter your Facebook access token: ")
    page_id = input("Enter your Facebook page ID: ")
    
    return {
        "access_token": access_token,
        "page_id": page_id
    }


def setup_twitter():
    """Setup Twitter API credentials"""
    print("\n🔧 Setting up Twitter/X API...")
    print("1. Go to https://developer.twitter.com/")
    print("2. Create a new app")
    print("3. Generate API keys and tokens")
    
    api_key = input("Enter your Twitter API key: ")
    api_secret = input("Enter your Twitter API secret: ")
    access_token = input("Enter your Twitter access token: ")
    access_token_secret = input("Enter your Twitter access token secret: ")
    bearer_token = input("Enter your Twitter bearer token: ")
    
    return {
        "api_key": api_key,
        "api_secret": api_secret,
        "access_token": access_token,
        "access_token_secret": access_token_secret,
        "bearer_token": bearer_token
    }


def setup_linkedin():
    """Setup LinkedIn API credentials"""
    print("\n🔧 Setting up LinkedIn API...")
    print("1. Go to https://www.linkedin.com/developers/")
    print("2. Create a new app")
    print("3. Get authorization and access token")
    
    access_token = input("Enter your LinkedIn access token: ")
    person_id = input("Enter your LinkedIn person ID: ")
    
    return {
        "access_token": access_token,
        "person_id": person_id
    }


def setup_openai():
    """Setup OpenAI API credentials"""
    print("\n🔧 Setting up OpenAI API...")
    print("1. Go to https://platform.openai.com/")
    print("2. Create an API key")
    
    api_key = input("Enter your OpenAI API key: ")
    
    return {
        "api_key": api_key
    }


def setup_content_mapping():
    """Setup content file mapping"""
    print("\n🔧 Setting up content file mapping...")
    print("Enter the names of your content files in Google Drive:")
    
    facebook_file = input("Facebook content file name (e.g., facebook_content.txt): ")
    twitter_file = input("Twitter content file name (e.g., twitter_content.txt): ")
    linkedin_file = input("LinkedIn content file name (e.g., linkedin_content.txt): ")
    
    return {
        "facebook": facebook_file,
        "twitter": twitter_file,
        "linkedin": linkedin_file
    }


def main():
    """Main setup function"""
    print("🚀 Social Media Posting Agent Setup")
    print("=" * 50)
    
    config = {}
    
    # Google Drive setup
    google_creds_path = setup_google_drive()
    if google_creds_path:
        folder_id = input("Enter your Google Drive folder ID where content files are stored: ")
        config["google_drive"] = {
            "credentials_file": google_creds_path,
            "content_folder_id": folder_id,
            "scopes": ["https://www.googleapis.com/auth/drive.readonly"]
        }
    
    # Social media platforms setup
    config["facebook"] = setup_facebook()
    config["twitter"] = setup_twitter()
    config["linkedin"] = setup_linkedin()
    config["openai"] = setup_openai()
    
    # Content mapping
    config["content_mapping"] = setup_content_mapping()
    
    # Schedule setup
    print("\n🔧 Setting up schedule...")
    schedule_time = input("Enter posting time (HH:MM format, e.g., 19:00): ")
    timezone = input("Enter timezone (e.g., Asia/Kolkata): ")
    
    config["schedule"] = {
        "time": schedule_time,
        "timezone": timezone
    }
    
    # Save configuration
    with open("config.json", "w") as f:
        json.dump(config, f, indent=2)
    
    print("\n✅ Setup completed!")
    print("📁 Configuration saved to config.json")
    print("\n🚀 You can now run the scheduler with:")
    print("python scheduler.py")
    print("\n🧪 Or test with:")
    print("python scheduler.py --test")


if __name__ == "__main__":
    main()
