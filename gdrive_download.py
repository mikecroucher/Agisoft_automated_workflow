import httplib2
import os
import io

from apiclient import discovery
from apiclient.http import MediaIoBaseDownload
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

#SCOPES determines the level of Google Drive permissions available to the script
#See https://developers.google.com/drive/v2/web/about-auth for details
SCOPES = 'https://www.googleapis.com/auth/drive.readonly'
CLIENT_SECRET_FILE = 'client_secrets.json'
APPLICATION_NAME = 'Drive API Python Quickstart'

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None
    
print(flags)

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'drive-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

credentials = get_credentials()
http = credentials.authorize(httplib2.Http())
drive_service = discovery.build('drive', 'v3', http=http)
dirname = 'Photogrammetry Group 3'

def find_id_of_dir(dirname):
    page_token = None
    file_id = None
    while True:
        response = drive_service.files().list(q="mimeType='application/vnd.google-apps.folder' and name='"+dirname+"'",
                                             spaces='drive',
                                             fields='nextPageToken, files(id, name)',
                                             pageToken=page_token).execute()
        for file in response.get('files', []):
            # Process change
            print('Found file: %s (%s)' % (file.get('name'), file.get('id')))
            file_id = file.get('id')
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break;
    return(file_id)

file_id = find_id_of_dir(dirname)
print(file_id)  

def download_file(file_id,filename):
    request = drive_service.files().get_media(fileId=file_id)
    fh = io.FileIO(filename,mode='wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("\r" + "#" * int(status.progress() * 100),end="")
    print()

def list_files(dir_id):
    page_token = None
    while True:
        response = drive_service.files().list(q="'" + dir_id + "' in parents",
                                             spaces='drive',
                                             fields='nextPageToken, files(id, name)',
                                             pageToken=page_token).execute()
        for file in response.get('files', []):
            # Process change
            print('Found file: %s (%s)' % (file.get('name'), file.get('id')))
            file_id = file.get('id')
            download_file(file_id,file.get('name'))
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break;
 
list_files(file_id)


        


 