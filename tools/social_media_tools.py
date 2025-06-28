from crewai_tools import BaseTool
import facebook
import tweepy
import requests
import json
from typing import Dict


class FacebookTool(BaseTool):
    name: str = "Facebook Poster"
    description: str = "Posts content to Facebook page"
    
    def __init__(self, config: Dict):
        super().__init__()
        self.config = config
        self.graph = facebook.GraphAPI(access_token=config['access_token'])
    
    def _run(self, content: str) -> str:
        """Post content to Facebook"""
        try:
            result = self.graph.put_object(
                parent_object=self.config['page_id'],
                connection_name='feed',
                message=content
            )
            return f"Successfully posted to Facebook. Post ID: {result['id']}"
        except Exception as e:
            return f"Error posting to Facebook: {str(e)}"


class TwitterTool(BaseTool):
    name: str = "Twitter Poster"
    description: str = "Posts content to Twitter/X"
    
    def __init__(self, config: Dict):
        super().__init__()
        self.config = config
        self.client = tweepy.Client(
            bearer_token=config['bearer_token'],
            consumer_key=config['api_key'],
            consumer_secret=config['api_secret'],
            access_token=config['access_token'],
            access_token_secret=config['access_token_secret'],
            wait_on_rate_limit=True
        )
    
    def _run(self, content: str) -> str:
        """Post content to Twitter"""
        try:
            # Ensure content is within Twitter's character limit
            if len(content) > 280:
                content = content[:277] + "..."
            
            response = self.client.create_tweet(text=content)
            return f"Successfully posted to Twitter. Tweet ID: {response.data['id']}"
        except Exception as e:
            return f"Error posting to Twitter: {str(e)}"


class LinkedInTool(BaseTool):
    name: str = "LinkedIn Poster"
    description: str = "Posts content to LinkedIn"
    
    def __init__(self, config: Dict):
        super().__init__()
        self.config = config
        self.headers = {
            'Authorization': f'Bearer {config["access_token"]}',
            'Content-Type': 'application/json',
            'X-Restli-Protocol-Version': '2.0.0'
        }
    
    def _run(self, content: str) -> str:
        """Post content to LinkedIn"""
        try:
            url = 'https://api.linkedin.com/v2/ugcPosts'
            
            post_data = {
                "author": f"urn:li:person:{self.config['person_id']}",
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
            
            response = requests.post(url, headers=self.headers, json=post_data)
            
            if response.status_code == 201:
                return f"Successfully posted to LinkedIn. Response: {response.json()}"
            else:
                return f"Error posting to LinkedIn: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"Error posting to LinkedIn: {str(e)}"
