from crewai_tools import BaseTool
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import json
import os
from typing import Dict, List


class GoogleDriveTool(BaseTool):
    name: str = "Google Drive Content Fetcher"
    description: str = "Fetches content from specified files in Google Drive"
    
    def __init__(self, config: Dict):
        super().__init__()
        self.config = config
        self.service = self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Google Drive API"""
        creds = None
        token_file = 'token.json'
        
        if os.path.exists(token_file):
            creds = Credentials.from_authorized_user_file(token_file, self.config['scopes'])
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.config['credentials_file'], self.config['scopes'])
                creds = flow.run_local_server(port=0)
            
            with open(token_file, 'w') as token:
                token.write(creds.to_json())
        
        return build('drive', 'v3', credentials=creds)
    
    def _run(self, filename: str) -> str:
        """Fetch content from a specific file in Google Drive"""
        try:
            # Search for the file in the specified folder
            query = f"name='{filename}' and parents in '{self.config['content_folder_id']}'"
            results = self.service.files().list(q=query, fields="files(id, name)").execute()
            files = results.get('files', [])
            
            if not files:
                return f"File '{filename}' not found in Google Drive"
            
            file_id = files[0]['id']
            
            # Download file content
            content = self.service.files().get_media(fileId=file_id).execute()
            return content.decode('utf-8')
            
        except Exception as e:
            return f"Error fetching content from Google Drive: {str(e)}"
