from __future__ import print_function
import os
import pickle
from typing import Dict
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from pydantic import Field, BaseModel
from langchain.tools import tool

SCOPES = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/documents'
]

CLIENT_SECRET_PATH = "<PATH_TO_CLIENT_SECRET_JSON>"  # TODO: Insert path to your client_secret.json
TOKEN_PATH = '<PATH_TO_TOKEN_PICKLE>'  # TODO: Insert path to your token.pickle
TEMPLATE_DOCUMENT_ID = "<YOUR_TEMPLATE_DOCUMENT_ID>"  # TODO: Insert your Google Docs template document ID
FOLDER_ID = "<YOUR_GOOGLE_DRIVE_FOLDER_ID>"  # TODO: Insert your Google Drive folder ID

class GoogleDocsReportTool:
    def __init__(self):
        self.creds = self.get_user_credentials()
        self.drive_service = build('drive', 'v3', credentials=self.creds)
        self.docs_service = build('docs', 'v1', credentials=self.creds)

    def get_user_credentials(self):
        creds = None
        if os.path.exists(TOKEN_PATH):
            with open(TOKEN_PATH, 'rb') as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    CLIENT_SECRET_PATH, SCOPES
                )
                creds = flow.run_local_server(port=0)
            with open(TOKEN_PATH, 'wb') as token:
                pickle.dump(creds, token)

        return creds


    def generate_meeting_report(self, data: Dict[str, str]) -> str:

        # Step 1: Copy the template
        copied_doc = self.drive_service.files().copy(
            fileId=TEMPLATE_DOCUMENT_ID,
            body={
                'name': f"Lettter",
                'parents': [FOLDER_ID]
            }
        ).execute()

        copied_doc_id = copied_doc.get('id')
        
        # Step 2: Create text replacements
        requests = []
        for key, value in data.items():
            requests.append({
                "replaceAllText": {
                    "containsText": {
                        "text": f"{{{{{key}}}}}",
                        "matchCase": True
                    },
                    "replaceText": value
                }
            })

        # Step 3: Execute batch update
        self.docs_service.documents().batchUpdate(
            documentId=copied_doc_id,
            body={"requests": requests}
        ).execute()

        return f"https://docs.google.com/document/d/{copied_doc_id}/edit"

def generate_meeting_report_tool(data: Dict[str, str]) -> str:
    tool_instance = GoogleDocsReportTool()
    return tool_instance.generate_meeting_report(data)

