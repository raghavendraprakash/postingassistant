from crewai import Crew, Process
from tasks import SocialMediaTasks
from agents import SocialMediaAgents
import json
from typing import Dict


class SocialMediaCrew:
    def __init__(self, config_path: str = "config.json"):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.agents = SocialMediaAgents(self.config)
        self.tasks = SocialMediaTasks(self.config)
    
    def create_crew(self) -> Crew:
        """Create and configure the CrewAI crew"""
        
        # Create agents
        content_manager = self.agents.content_manager_agent()
        facebook_agent = self.agents.facebook_agent()
        twitter_agent = self.agents.twitter_agent()
        linkedin_agent = self.agents.linkedin_agent()
        coordinator = self.agents.coordinator_agent()
        
        # Create tasks
        fetch_content = self.tasks.fetch_content_task()
        post_facebook = self.tasks.post_to_facebook_task()
        post_twitter = self.tasks.post_to_twitter_task()
        post_linkedin = self.tasks.post_to_linkedin_task()
        coordinate = self.tasks.coordination_task()
        
        # Set task dependencies
        post_facebook.context = [fetch_content]
        post_twitter.context = [fetch_content]
        post_linkedin.context = [fetch_content]
        coordinate.context = [fetch_content, post_facebook, post_twitter, post_linkedin]
        
        # Create crew
        crew = Crew(
            agents=[content_manager, facebook_agent, twitter_agent, linkedin_agent, coordinator],
            tasks=[fetch_content, post_facebook, post_twitter, post_linkedin, coordinate],
            process=Process.sequential,
            verbose=2
        )
        
        return crew
    
    def run_posting_workflow(self):
        """Execute the social media posting workflow"""
        try:
            print("🚀 Starting Social Media Posting Workflow...")
            crew = self.create_crew()
            result = crew.kickoff()
            
            print("✅ Social Media Posting Workflow Completed!")
            print("📊 Results:")
            print(result)
            
            return result
            
        except Exception as e:
            print(f"❌ Error in posting workflow: {str(e)}")
            return None


if __name__ == "__main__":
    # Test run
    social_crew = SocialMediaCrew()
    social_crew.run_posting_workflow()
