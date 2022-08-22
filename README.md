# CourseWork

Программа:

1. Получает фотографии из указанного альбома Vkontakte;
2. Сохраняет полученные фотографии максимального размера(ширина/высота в пикселях) на Yandex Disk/Google Drive;
3. Для имени фотографий используется количество лайков. Если количество лайков совпадает, добавляется дата публикации фотографии;
4. Информация по фотографиям сохраняется в json-файл с результатами.

# Структура проекта

* `google_drive` - функционал для работы с Google Drive;
* `yandex_disk` - функционал для работы с Yandex Disk;
* `progress_bar` - функционал прогресс-бара;
* `vkontakte` - функционал для работы с Vkontakte;
* `main` - главный модуль проекта.

Перед использованием необходимо заполнить соответствующими значенями файлы `tokens.ini` (токены для Vkontakte и Yandex Disk) и `cred.json` (данные для Google Drive)
# Usage

```
main.py [-h] [-file FILE] [-album_id ALBUM_ID] [-num NUM] {id,sn} identifier {yd,gd} save_folder

Get a photo from vk and save it to yandex disk or google drive.

positional arguments:
  {id,sn}             photo acquisition method: by owner id or by screen name
  identifier          owner id or screen name
  {yd,gd}             location for saving photos: Yandex Disk or Google drive
  save_folder         path to the directory on Yandex Disk or Google Drive to save files

optional arguments:
  -h, --help          show this help message and exit
  -file FILE          path to ini-file with tokens and api versions
  -album_id ALBUM_ID  user album id
  -num NUM            number of saved photos
```
Примеры:
1. `python3.8 main.py id <user_id> yd <save_folder> -file=<file_name>.ini -album_id=<album_id> -num=10`  
Программа возьмёт 10 фотографий пользователя `user_id` из альбома `album_id` и сохранит их на `Yandex Disk` в каталог `save_folder`. Токены считаются из файла `<file_name>.ini` 
2. `python3.8 main.py sn <screen name> gd <save_folder>`  
Программа возьмёт 5 (исп. значение по умолчанию) фотографий пользователя `screen name` из профиля (исп. значение по умолчанию) и сохранит их на `Google Drive` в каталог `save_folder`. Токены считаются из файла `tokens.ini` в корне проекта. 
