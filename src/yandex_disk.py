import json
import sys
import traceback

import requests
from requests.exceptions import HTTPError

from progress_bar import ProgressBar


class YandexDisk:
    yd_url = 'https://cloud-api.yandex.net/v1/disk/'

    def __init__(self, ya_token):
        self.yandex_params = {'Authorization': f'OAuth {ya_token}'}

    def create_directory_on_yandex_disk(self, dir_name):
        """Сreates a new directory on Yandex disk

        Keyword Arguments:
            - dir_name -- directory to be created

        """

        create_dir_url = self.yd_url + 'resources'
        create_dir_params = {'path': dir_name}
        try:
            resp = requests.put(create_dir_url, headers={**self.yandex_params}, params={**create_dir_params})
            resp.raise_for_status()
        except HTTPError as exc:
            code = exc.response.status_code
            if code != 409:
                traceback.print_exc()
                print(resp.json()["message"])
                sys.exit(1)

    def upload_photo_to_yandex_disk(self, file_path, url):
        """Uploads a photo to Yandex Disk

        Keyword Arguments:
            - file_path -- path to the file on Yandex Disk
            - url -- link to download file

        """        

        upload_url = self.yd_url + 'resources/upload'
        upload_params = {
                'path': file_path,
                'url': url
        }
        try:
            resp = requests.post(upload_url, headers={**self.yandex_params}, params={**upload_params})
            resp.raise_for_status()
        except HTTPError:
            traceback.print_exc()
            print(resp.json()["message"])
            sys.exit(1)            

    def parse_vkontakte_response_and_make_backup_photo_on_yandex_disk(self, resp, dir_name, number_of_photos_to_save=5):
        """Uploads a photo to Yandex Disk

        Keyword Arguments:
            - resp -- VKontakte data with photo information
            - dir_name -- directory on Yandex Disk in which you want to save the photo
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
                self.upload_photo_to_yandex_disk(f'{dir_name}/{image_likes}-{item["date"]}.jpg', image_url)
            else:
                self.upload_photo_to_yandex_disk(f'{dir_name}/{image_likes}.jpg', image_url)
                photos_name.append(f'{image_likes}.jpg')

            if number_of_photos_to_save < len(resp['response']['items']):
                prog_bar.printProgressBar(i, number_of_photos_to_save)
            else:
                prog_bar.printProgressBar(i, len(resp['response']['items']))

            if number_of_photos_to_save == i:
                break

        with open('result.json', 'w') as file:
            json.dump(json_result, file, indent=4)