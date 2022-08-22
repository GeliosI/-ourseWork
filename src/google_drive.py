import io
import json
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError as GoogleHttpError
from googleapiclient.http import MediaIoBaseUpload
import requests

from progress_bar import ProgressBar


class GoogleDrive:
    gd_url = ['https://www.googleapis.com/auth/drive']    

    def __init__(self):
        self.creds = None

        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', self.gd_url)

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                self.flow = InstalledAppFlow.from_client_secrets_file(
                    './../cred.json', self.gd_url)
                self.creds = self.flow.run_local_server(port=0)

            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())

        self.service = build('drive', 'v3', credentials=self.creds)        

    def create_directory_on_google_drive(self, dir_name):
        """Сreates a new directory on Google Drive

        Keyword Arguments:
            - dir_name -- directory to be created

        """

        try:
            file_metadata = {
                'name': dir_name,
                'mimeType': 'application/vnd.google-apps.folder',
            }
            file = self.service.files().create(body=file_metadata,
                                                fields='id').execute()                       
            return file.get("id")                                        
        except GoogleHttpError as error:
            print(f'An error occurred: {error}')                       
            
    def upload_photo_to_google_drive(self, file_path, dir_id, url):
        """Uploads a photo to Google Drive

        Keyword Arguments:
            - file_path -- path to the file on Google Drive
            - dir_id -- id of the directory in which the files are uploaded
            - url -- link to download file

        """   

        vk_image = requests.get(url)
        fh = io.BytesIO()
        fh.write(vk_image.content)

        media = MediaIoBaseUpload(fh, mimetype='image/jpg')    

        file_metadata = { 
            'name' : file_path,
            'parents': [dir_id]
        }

        self.service.files().create(
            body=file_metadata, media_body=media, fields='id').execute()

    def parse_vkontakte_response_and_make_backup_photo_on_google_drive(self, resp, dir_id, number_of_photos_to_save=5):
        """Uploads a photo to Google Drive

        Keyword Arguments:
            - resp -- VKontakte data with photo information
            - dir_name -- directory on Google Drive in which you want to save the photo
            - number_of_photos_to_save - number of saved photos

        """           

        prog_bar = ProgressBar()
        prog_bar.printProgressBar(0, len(resp['response']['items']))
        json_result = []
        photos_name = []
        image_type = ""
        image_url = ""

        for i, item in enumerate(resp['response']['items'], 1):
            image_likes = item['likes']['count']
            max_image_size = -1
            for size in item['sizes']:
                image_size = size['height'] + size['width']
                if image_size > max_image_size:
                    max_image_size = image_size
                    image_url = size['url']
                    image_type = size['type']            

            json_result.append({'file_name': f'{image_likes}.jpg', 'size': image_type})
            
            if f'{image_likes}.jpg' in photos_name:
                self.upload_photo_to_google_drive(f'{dir_id}/{image_likes}-{item["date"]}.jpg', dir_id, image_url)
            else:
                self.upload_photo_to_google_drive(f'{dir_id}/{image_likes}.jpg', dir_id, image_url)
                photos_name.append(f'{image_likes}.jpg')

            if number_of_photos_to_save < len(resp['response']['items']):
                prog_bar.printProgressBar(i, number_of_photos_to_save)
            else:
                prog_bar.printProgressBar(i, len(resp['response']['items']))

            if number_of_photos_to_save == i:
                break
            
            if number_of_photos_to_save == i:
                break

        with open('result.json', 'w') as file:
            json.dump(json_result, file, indent=4)