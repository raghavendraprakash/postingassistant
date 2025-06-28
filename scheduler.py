import schedule
import time
import pytz
from datetime import datetime
from crew import SocialMediaCrew
import json
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('social_media_posting.log'),
        logging.StreamHandler()
    ]
)

class SocialMediaScheduler:
    def __init__(self, config_path: str = "config.json"):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.crew = SocialMediaCrew(config_path)
        self.timezone = pytz.timezone(self.config['schedule'].get('timezone', 'Asia/Kolkata'))
    
    def run_posting_job(self):
        """Job function that runs the social media posting workflow"""
        try:
            current_time = datetime.now(self.timezone)
            logging.info(f"🕐 Starting scheduled social media posting at {current_time}")
            
            result = self.crew.run_posting_workflow()
            
            if result:
                logging.info("✅ Scheduled posting completed successfully")
            else:
                logging.error("❌ Scheduled posting failed")
                
        except Exception as e:
            logging.error(f"❌ Error in scheduled posting: {str(e)}")
    
    def start_scheduler(self):
        """Start the scheduler with the configured time"""
        schedule_time = self.config['schedule']['time']
        
        # Schedule the job
        schedule.every().day.at(schedule_time).do(self.run_posting_job)
        
        logging.info(f"📅 Scheduler started. Posts will be published daily at {schedule_time} {self.config['schedule'].get('timezone', 'Asia/Kolkata')}")
        logging.info("🔄 Scheduler is running. Press Ctrl+C to stop.")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
                
        except KeyboardInterrupt:
            logging.info("🛑 Scheduler stopped by user")
    
    def run_once(self):
        """Run the posting workflow once (for testing)"""
        logging.info("🧪 Running one-time posting workflow for testing...")
        self.run_posting_job()


def main():
    """Main function to start the scheduler"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Social Media Posting Scheduler')
    parser.add_argument('--test', action='store_true', help='Run once for testing')
    parser.add_argument('--config', default='config.json', help='Path to config file')
    
    args = parser.parse_args()
    
    scheduler = SocialMediaScheduler(args.config)
    
    if args.test:
        scheduler.run_once()
    else:
        scheduler.start_scheduler()


if __name__ == "__main__":
    main()
