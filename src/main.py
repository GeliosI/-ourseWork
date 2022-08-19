import argparse
import configparser
import sys
import traceback

from vkontakte import Vkontakte
from yandex_disk import YandexDisk


def get_tokens_and_api_versions(file):
    config = configparser.ConfigParser()
    try:
        with open(file):
            config.read(file)
    except FileNotFoundError:
        traceback.print_exc()
        print('Specify the correct path to the ini-file')
        sys.exit(1)

    try:
        yd_token = config['YandexDisk']['token']
        vk_token = config['Vkontakte']['token']
        vk_api_version = config['Vkontakte']['api_version']
    except KeyError:
        traceback.print_exc()
        print('ini-file is not well formed')
        sys.exit(1)

    return yd_token, vk_token, vk_api_version


def get_args():
    parser = argparse.ArgumentParser(description="Get a photo from vk and save it to yandex disk.")

    parser.add_argument('method', choices=['id', 'sn'],
                        help='photo acquisition method: by owner id or by screen name')
    parser.add_argument('identifier',
                        help='owner id or screen name')
    parser.add_argument('yd_folder',
                        help='path to the directory on Yandex Disk to save files')                        
    parser.add_argument('-file', default='./../tokens.ini', 
                        help='path to ini-file with tokens and api versions')
    parser.add_argument('-album_id', default='profile', 
                        help='user album id')
    parser.add_argument('-num', type=int, default=5, 
                        help='number of saved photos')                        
    return parser.parse_args()


def vk_photo_backup():
    args = get_args()
    yd_token, vk_token, vk_api_version = get_tokens_and_api_versions(args.file)
    vk = Vkontakte(vk_token, vk_api_version)

    if args.method == 'id':
        id = args.identifier
        vk_resp = vk.get_photos_by_owner_id(id, args.album_id)
    else:
        screen_name = args.identifier
        vk_resp = vk.get_photos_by_screen_name(screen_name, args.album_id)

    yd = YandexDisk(yd_token)
    yd.create_directory_on_yandex_disk(args.yd_folder)
    yd.parse_vkontakte_response_and_make_backup_photo_on_yandex_disk(vk_resp, args.yd_folder, args.num)


if __name__ == '__main__':
    vk_photo_backup()