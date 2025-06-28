from crewai import Agent
from tools.google_drive_tool import GoogleDriveTool
from tools.social_media_tools import FacebookTool, TwitterTool, LinkedInTool
from langchain_openai import ChatOpenAI
from typing import Dict


class SocialMediaAgents:
    def __init__(self, config: Dict):
        self.config = config
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            api_key=config['openai']['api_key']
        )
        
        # Initialize tools
        self.google_drive_tool = GoogleDriveTool(config['google_drive'])
        self.facebook_tool = FacebookTool(config['facebook'])
        self.twitter_tool = TwitterTool(config['twitter'])
        self.linkedin_tool = LinkedInTool(config['linkedin'])
    
    def content_manager_agent(self) -> Agent:
        """Agent responsible for fetching and managing content from Google Drive"""
        return Agent(
            role='Content Manager',
            goal='Fetch and organize content from Google Drive for social media posting',
            backstory="""You are a skilled content manager who specializes in organizing 
            and preparing content for social media distribution. You have access to Google Drive 
            and can retrieve specific content files for different social media platforms.""",
            tools=[self.google_drive_tool],
            llm=self.llm,
            verbose=True
        )
    
    def facebook_agent(self) -> Agent:
        """Agent responsible for posting to Facebook"""
        return Agent(
            role='Facebook Social Media Manager',
            goal='Post engaging content to Facebook page',
            backstory="""You are a Facebook social media specialist who knows how to craft 
            engaging posts that resonate with Facebook audiences. You understand Facebook's 
            best practices and can adapt content accordingly.""",
            tools=[self.facebook_tool],
            llm=self.llm,
            verbose=True
        )
    
    def twitter_agent(self) -> Agent:
        """Agent responsible for posting to Twitter/X"""
        return Agent(
            role='Twitter Social Media Manager',
            goal='Post concise and engaging content to Twitter/X',
            backstory="""You are a Twitter/X specialist who excels at creating concise, 
            impactful tweets. You understand the platform's character limits and trending 
            topics, and can adapt content to fit Twitter's fast-paced environment.""",
            tools=[self.twitter_tool],
            llm=self.llm,
            verbose=True
        )
    
    def linkedin_agent(self) -> Agent:
        """Agent responsible for posting to LinkedIn"""
        return Agent(
            role='LinkedIn Professional Content Manager',
            goal='Post professional and thought-leadership content to LinkedIn',
            backstory="""You are a LinkedIn content specialist who understands professional 
            networking and thought leadership. You can craft content that establishes 
            authority and engages with professional audiences.""",
            tools=[self.linkedin_tool],
            llm=self.llm,
            verbose=True
        )
    
    def coordinator_agent(self) -> Agent:
        """Agent responsible for coordinating the entire posting process"""
        return Agent(
            role='Social Media Coordinator',
            goal='Coordinate and oversee the entire social media posting process',
            backstory="""You are an experienced social media coordinator who manages 
            multiple platforms and ensures consistent brand messaging across all channels. 
            You coordinate with content managers and platform specialists to execute 
            successful social media campaigns.""",
            llm=self.llm,
            verbose=True
        )
