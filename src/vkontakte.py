import sys
import traceback

import requests


class VkApiException(Exception):
   pass


class Vkontakte:
    vk_url = 'https://api.vk.com/method/'

    def __init__(self, vk_token, vk_api_version):
        """Object for backup photos from vkontakte to yandex disk.

        Keyword Arguments:
            - vk_token -- vkontakte user token
            - vk_api_version -- vkontakte api version

        """

        self.vk_params = {
            'access_token': vk_token,
            'v': vk_api_version    
        }
        
    def get_owner_id_by_screen_name(self, screen_name):
        """Returns the user id by screen name

        Keyword Arguments:
            - screen_name -- vkontakte user screen name

        """

        user_id_url = self.vk_url + 'utils.resolveScreenName'
        user_id_params = {'screen_name': screen_name}

        try:
            resp = requests.get(user_id_url, params={**self.vk_params, **user_id_params}).json()
            if 'object_id' not in resp['response']:
                raise VkApiException()
        except VkApiException:
            traceback.print_exc()
            print('VK API Error: User with this screen name does not exist')
            sys.exit(1)  

        return resp['response']['object_id']

    def get_photos_by_owner_id(self, owner_id, album_id='profile', extended=1):
        """Returns a description of the user's album by its id

        Keyword Arguments:
            - owner_id -- vkontakte album owner id
            - screen_name -- vkontakte user album id
            - extended -- if extended=1, returns additional fields likes, comments, tags, can_comment, reposts  

        """

        photos_get_url = self.vk_url + 'photos.get'
        photos_get_params = {
            'owner_id': owner_id,
            'album_id': album_id,
            'extended': extended
        }
        try:
            resp = requests.get(photos_get_url, params={**self.vk_params, **photos_get_params}).json()
            if 'error' in resp:
                raise VkApiException()
        except VkApiException:
            traceback.print_exc()
            print(f'VK API Error: {resp["error"]["error_msg"]}')
            sys.exit(1)   

        return resp

    def get_photos_by_screen_name(self, screen_name, album_id='profile', extended=1):
        """Returns a description of the user's album by its screen_name

        Keyword Arguments:
            - screen_name -- vkontakte album screen name
            - album_id -- vkontakte user album id
            - extended -- if extended=1, returns additional fields likes, comments, tags, can_comment, reposts     

        """

        owner_id = self.get_owner_id_by_screen_name(screen_name)
        photos_get_url = self.vk_url + 'photos.get'
        photos_get_params = {
            'owner_id': owner_id,
            'album_id': album_id,
            'extended': extended
        }
        try:
            resp = requests.get(photos_get_url, params={**self.vk_params, **photos_get_params}).json()
            if 'error' in resp:
                raise VkApiException()
        except VkApiException:
            traceback.print_exc()
            print(f'VK API Error: {resp["error"]["error_msg"]}')
            sys.exit(1)                 

        return resp