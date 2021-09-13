import pickle
import os

from abc import ABC, abstractmethod

from googleapiclient.discovery import build  # type: ignore
from google_auth_oauthlib.flow import InstalledAppFlow # type: ignore
from google.auth.transport.requests import Request # type: ignore
from google.auth.exceptions import RefreshError # type: ignore

class Service(ABC):
    
    @abstractmethod
    def _get_creds(self) -> 'Credentials':
        ...

class GoogleService(Service):
    
    def __init__(self, 
                 creds_path: str, 
                 secrets_path: str, 
                 scopes: str,
                 service_name: str,
                 service_version: str
                ):
        self.creds_path = creds_path
        self.secrets_path = secrets_path
        self.scopes = scopes
        self.service_name = service_name,
        self.service_version = service_version
        
        self.creds = self._get_creds()
        self.service = build(service_name, service_version, credentials=self.creds)
    
    def _get_creds(self) -> 'Credentials':
        creds = None
        if os.path.exists(self.creds_path):
            with open(self.creds_path, 'rb') as f:
                creds =  pickle.load(f)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except RefreshError as e:
                    flow = InstalledAppFlow.from_client_secrets_file(self.secrets_path, scopes=self.scopes)
                    creds = flow.run_local_server()
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.secrets_path, scopes=self.scopes)
                creds = flow.run_local_server()
            with open(self.creds_path, 'wb') as f:
                pickle.dump(creds, f)
        
        return creds