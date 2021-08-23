from pprint import pprint
import requests


# Получение ТОКЕНА. Если нет прикрепленного файла, используем ручной ввод.
# with open('token_VK.txt', 'r') as file_object:
#     token_VK = file_object.read().strip()
token_VK = input('Введите свой ТОКЕН для ВК ')
# with open('token_yandex.txt', 'r') as file_object:
#     token_yandex = file_object.read().strip()
token_yandex = input('Введите свой ТОКЕН для Яндекс Диска ')

# Запрос id аккаунта. 
owner_id = input('Введите id аккаунта, чьи фото мы копируем: ')

# Работа с ВК
class VkUser:
  url = 'https://api.vk.com/method/'

  def __init__(self, token, version):
    self.params = {
      'access_token': token,
      'v': version
    }
# Получение фотографий из профиля. Только аватарки.
  def search_photos(self, owner_id, sorting=0):
    photos_search_url = self.url + 'photos.get'
    photos_search_params = {
      'count': 50,
      'owner_id': owner_id,
      'extended': 1,
      'album_id': 'profile'
    }
    req = requests.get(photos_search_url, params={**self.params, **photos_search_params}).json()
    return req['response']['items']

# Работа по поиску фото профиля
vk_client = VkUser(token_VK, '5.131')
i = 0
photos_json = vk_client.search_photos(owner_id)
photos_count = len(photos_json)
new_json = []

# Запрашиваю количество фоток для скачивания
print(f'У аккаунта {owner_id} в профиле {photos_count} фотографий')
photos_count_need = int(input('Сколько фотографий мы хотим скопировать: '))

if photos_count_need < photos_count:
  photos_count = photos_count_need
else:
  print('Скопируем сколько есть, больше никак')

# Создаю новый json по образцу
while i < photos_count:
  photos_dict = {}
  likes = photos_json[i]['likes']['count']
  size_len = len(photos_json[i]['sizes']) - 1 
  size = photos_json[i]['sizes'][size_len]
  photos_dict['file name'] = likes
  photos_dict['size'] = size
  new_json.append(photos_dict)
  i += 1

# Принеобходимости можем посмотреть список фотографий и информацию по размеру:
pprint(new_json)

# Работа с Яндексом 
class YaUploader:
  API_BASE_URL = "https://cloud-api.yandex.net:443"

  def __init__(self, token: str):
    self.token = token
    self.headers = {
      'Authorization': self.token
    }

# Создание новой папки
  def new_folder(self, name_folder):
    req = requests.put(self.API_BASE_URL + '/v1/disk/resources?path=' + name_folder, headers=self.headers)
    req_url = req.json()["href"]
    return req_url

# Метод для загрузки файла по ссылке в папку Яндекс диска
  def upload(self, name_folder, name_file, path_to_file: str):
    name_folder_file = f'{name_folder}/{name_file}.jpeg'
    params = {
      'path': name_folder_file,
      'url' : path_to_file
    }
    requests.post(self.API_BASE_URL + '/v1/disk/resources/upload', params=params, headers=self.headers)

# Спрашиваю как назвать папку:
uploader = YaUploader(token_yandex)
name_folder = input(f'Как назвать папку? ')
url_folder = uploader.new_folder(name_folder)
x = 0
# Загружаю фото поочереди по ссылке из созданного json файла
while x < photos_count:
  name_file = new_json[x]['file name']
  path_to_file = new_json[x]['size']['url']
  uploader.upload(name_folder, name_file, path_to_file)
  x += 1
  print(f'Файл {name_file} загружен')
print('ГОТОВО, Спасибо за внимание!')