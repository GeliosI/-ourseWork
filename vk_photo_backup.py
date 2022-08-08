import requests
import json


class VkPhotoBackup:
    vk_url = 'https://api.vk.com/method/'
    yd_url = 'https://cloud-api.yandex.net/v1/disk/'

    def __init__(self, vk_token, vk_api_version, ya_token):
        self.yandex_params = {
            'Authorization': f'OAuth {ya_token}'
        }

        self.vk_params = {
            'access_token': vk_token,
            'v': vk_api_version    
        }
        
    def get_photos(self, owner_id, album_id='profile', extended=1):
        '''
        Метод возвращает список фотографий в альбоме.

        owner_id - id владельца альбома
        album_id - id альбома, по умолчанию берём аватарки
        extended - если 1, возвращает дополнительные поля likes, comments, tags, can_comment, reposts
        '''

        photos_get_url = self.vk_url + 'photos.get'
        photos_get_params = {
            'owner_id': owner_id,
            'album_id': album_id,
            'extended': extended
        }

        resp = requests.get(photos_get_url, params={**self.vk_params, **photos_get_params}).json()

        return resp

    def create_directory_on_yandex_disk(self, dir_name):
        '''
        Метод создаёт новый каталог на Яндекс Диске

        dir_name - каталог, который необходимо создать
        '''

        create_dir_url = self.yd_url + 'resources'
        create_dir_params = {'path': dir_name}

        resp = requests.put(create_dir_url, headers={**self.yandex_params}, params={**create_dir_params})

        return resp.status_code

    def printProgressBar (self, iteration, total, length = 100):
        '''
        Метод - реализация прогресс-бара

        iteration - номер итерации
        total - общее количество итераций
        length - длина прогресс-бара
        '''

        percent = ('{0:.1f}').format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = '█' * filledLength + '-' * (length - filledLength)
        print(f'Progress: |{bar}| {percent}% Complete', end = '\r')

        if iteration == total: 
            print()

    def upload_photo_to_yandex_disk(self, file_path, url):
        '''
        Метод загружает фото на Яндекс Диск

        file_path - путь до файла на Яндекс Диске
        url - ссылка на загружаемый файл
        '''
        upload_url = self.yd_url + 'resources/upload'
        upload_params = {
                'path': file_path,
                'url': url
                }

        resp = requests.post(upload_url, headers={**self.yandex_params}, params={**upload_params})

        return resp.status_code

    def parses_response_and_upload_photo_to_yandex_disk(self, resp, dir_name, number_of_photos_to_save=5):
        '''
        Метод загружает фото на Яндекс Диск и подготавливает json-файл с описанием загруженных фото

        resp - данные с информацией о фото
        dir_name - каталог, в которых необходимо сохранить фото
        '''

        json_result = []
        photos_name = []

        status_code = self.create_directory_on_yandex_disk(dir_name)

        if status_code!=201 and status_code!=409:
            return status_code

        self.printProgressBar(0, len(resp['response']['items']))

        for i, item in enumerate(resp['response']['items'], 1):
            image_likes = item['likes']['count']
            image_max_size = 0
            image_url = str
            image_type = str

            for size in item['sizes']:
                if size['height']+size['width'] > image_max_size:
                    image_max_size = size['height'] + size['width']
                    image_url = size['url']
                    image_type = size['type']            

            json_result.append({'file_name': f'{image_likes}.jpg', 'size': image_type})
            
            if f'{image_likes}.jpg' in photos_name:
                self.upload_photo_to_yandex_disk(f'{dir_name}/{image_likes}-{item["date"]}.jpg', image_url)
            else:
                self.upload_photo_to_yandex_disk(f'{dir_name}/{image_likes}.jpg', image_url)
                photos_name.append(f'{image_likes}.jpg')

            if number_of_photos_to_save < len(resp['response']['items']):
                self.printProgressBar(i, number_of_photos_to_save)
            else:
                self.printProgressBar(i, len(resp['response']['items']))
                
            if number_of_photos_to_save == i:
                break

        with open('result.json', 'w') as file:
            json.dump(json_result, file)


if __name__ == '__main__':
    with open('vk_token.txt') as vk_token_file, \
            open('ya_token.txt') as ya_toke_file:
        vk_token = vk_token_file.read().strip()
        ya_token = ya_toke_file.read().strip()
        
    vk_client = VkPhotoBackup(vk_token, '5.131', ya_token)

    # Передать id пользователя и album_id (опционально)
    resp = vk_client.get_photos('')

    # Передать название каталога, в который будут сохраняться фото. Опционально можно передать кол-во сохраняемых фото
    vk_client.parses_response_and_upload_photo_to_yandex_disk(resp, '')
