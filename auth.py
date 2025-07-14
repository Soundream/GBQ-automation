#!/usr/bin/env python3
"""
BigQuery Authentication Module
Handles Google Cloud authentication using gcloud CLI.
"""

from google.cloud import bigquery
from google.auth import default

class BigQueryAuth:
    def __init__(self):
        self.client = None
        self.project = None
    
    def authenticate(self):
        """
        Authenticate using Application Default Credentials (gcloud CLI).
        Silently performs authentication without verbose output.
        
        Returns:
            bool: True if authentication successful, False otherwise
        """
        # Suppress specific warning from google-auth
        import warnings
        warnings.filterwarnings("ignore", "Your application has authenticated using end user credentials")
        
        try:
            # Use Application Default Credentials silently
            credentials, project = default()
            
            if not credentials:
                print("ERROR: No valid credentials found. Run 'gcloud auth application-default login' first.")
                return False
            
            # Initialize BigQuery client
            self.client = bigquery.Client(credentials=credentials, project=project)
            self.project = project
            return True
            
        except Exception as e:
            print(f"Authentication error: {e}")
            return False
    
    def get_client(self):
        """
        Get the authenticated BigQuery client.
        
        Returns:
            google.cloud.bigquery.Client: Authenticated BigQuery client
        """
        if not self.client:
            raise Exception("Not authenticated. Please call authenticate() first.")
        return self.client 