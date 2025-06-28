from crewai import Task
from agents import SocialMediaAgents
from typing import Dict


class SocialMediaTasks:
    def __init__(self, config: Dict):
        self.config = config
        self.agents = SocialMediaAgents(config)
    
    def fetch_content_task(self) -> Task:
        """Task to fetch content from Google Drive"""
        return Task(
            description=f"""
            Fetch content from Google Drive for social media posting.
            
            Retrieve the following files from the designated Google Drive folder:
            - Facebook content: {self.config['content_mapping']['facebook']}
            - Twitter content: {self.config['content_mapping']['twitter']}
            - LinkedIn content: {self.config['content_mapping']['linkedin']}
            
            Organize the content and prepare it for distribution to respective social media platforms.
            Ensure each piece of content is appropriate for its target platform.
            """,
            agent=self.agents.content_manager_agent(),
            expected_output="A structured report containing content for each social media platform"
        )
    
    def post_to_facebook_task(self) -> Task:
        """Task to post content to Facebook"""
        return Task(
            description=f"""
            Post the Facebook content to the Facebook page.
            
            Use the content retrieved for Facebook and adapt it if necessary to:
            - Ensure it's engaging and appropriate for Facebook audience
            - Include relevant hashtags if applicable
            - Maintain the brand voice and messaging
            
            Content file: {self.config['content_mapping']['facebook']}
            """,
            agent=self.agents.facebook_agent(),
            expected_output="Confirmation of successful Facebook post with post ID"
        )
    
    def post_to_twitter_task(self) -> Task:
        """Task to post content to Twitter/X"""
        return Task(
            description=f"""
            Post the Twitter content to Twitter/X account.
            
            Use the content retrieved for Twitter and ensure it:
            - Stays within the 280 character limit
            - Uses appropriate hashtags and mentions
            - Is engaging and concise
            - Fits Twitter's fast-paced environment
            
            Content file: {self.config['content_mapping']['twitter']}
            """,
            agent=self.agents.twitter_agent(),
            expected_output="Confirmation of successful Twitter post with tweet ID"
        )
    
    def post_to_linkedin_task(self) -> Task:
        """Task to post content to LinkedIn"""
        return Task(
            description=f"""
            Post the LinkedIn content to LinkedIn profile.
            
            Use the content retrieved for LinkedIn and ensure it:
            - Maintains a professional tone
            - Provides value to professional network
            - Establishes thought leadership
            - Uses appropriate professional hashtags
            
            Content file: {self.config['content_mapping']['linkedin']}
            """,
            agent=self.agents.linkedin_agent(),
            expected_output="Confirmation of successful LinkedIn post with post details"
        )
    
    def coordination_task(self) -> Task:
        """Task to coordinate the entire posting process"""
        return Task(
            description="""
            Coordinate the entire social media posting process.
            
            Oversee the execution of all posting tasks and ensure:
            - All content is fetched successfully from Google Drive
            - Posts are made to all three platforms (Facebook, Twitter, LinkedIn)
            - Any errors are handled appropriately
            - A comprehensive report is generated
            
            Provide a summary of all posting activities and their status.
            """,
            agent=self.agents.coordinator_agent(),
            expected_output="A comprehensive report of all social media posting activities and their status"
        )
