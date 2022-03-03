from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/drive']


def gdrive_auth():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds


def gdrive_create_subdir(drive_service, parent_folder_id, name):
    file_metadata = {
        "name": name,
        "mimeType": "application/vnd.google-apps.folder",
        "parents": [parent_folder_id]
    }
    file = drive_service.files().create(body=file_metadata, supportsAllDrives=True,
                                        fields="id").execute()
    print(f"Directory created: {name}")
    return (file.get('id'))


def main():
    creds = gdrive_auth()

    try:
        service = build('drive', 'v3', credentials=creds)
        episode_number = input("Episode Number: ")
        episode_title = input("Episode Title: ")
        episode_name = f"CTS {episode_number}: {episode_title}"
        episode_folder_id = gdrive_create_subdir(
            service, "1jBzOTdeIqSCjMs22N_R7QTitKv-boflX", episode_name)
        gdrive_create_subdir(service, episode_folder_id, "01 Audio")
        gdrive_create_subdir(service, episode_folder_id, "02 Graphics")
        gdrive_create_subdir(service, episode_folder_id, "03 Video")
        gdrive_create_subdir(service, episode_folder_id, "04 Shownotes")

    except HttpError as error:
        print(f'An error occurred: {error}')


if __name__ == '__main__':
    main()
