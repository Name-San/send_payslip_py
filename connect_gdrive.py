from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle

# Define the scope for accessing Google Drive
SCOPES = ['https://www.googleapis.com/auth/drive']

import os
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/drive.file']

def authenticate_user(user_id):
    """Authenticate a user and save their credentials separately."""
    token_file = f'tokens/{user_id}_token.pickle'
    creds = None

    # Check if user's token exists
    if os.path.exists(token_file):
        with open(token_file, 'rb') as token:
            creds = pickle.load(token)

    # If no valid credentials, perform OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the user
        os.makedirs('tokens', exist_ok=True)
        with open(token_file, 'wb') as token:
            pickle.dump(creds, token)

    return build('drive', 'v3', credentials=creds)

def upload_file_to_drive(file_path, user_id, folder_id='1xEqyKg7WC5t3QVmgfZgw26BCLBQ9C4Um'):
    service = authenticate_user(user_id)
    file_metadata = {'name': os.path.basename(file_path)}
    if folder_id:
        file_metadata['parents'] = [folder_id]
    media = MediaFileUpload(file_path, resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f"File uploaded successfully. File ID: {file.get('id')}")

# Example usage
if __name__ == '__main__':
    file_path = 'example.txt'  # Replace with the path of the file to upload
    upload_file_to_drive(file_path, user_id='user2')