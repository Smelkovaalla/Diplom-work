from pprint import pprint
import requests

# Работа с ВК
class VkUser:
  url = 'https://api.vk.com/method/'

  def __init__(self, token, version):
    self.params = {
      'access_token': token,
      'v': version
    }

# Поиск id номера в случае, если его нет
  def search_id(self, user_ids):
    search_id_url = self.url + 'users.search'
    search_id_params = {
      'q': user_ids,
      'fields' : id
    }
    req = requests.get(search_id_url, params={**self.params, **search_id_params}).json()

    if req['response']['count'] == 0:
      print('Такого аккаунта не существует')
      return exit
    else:
      owner_id = req['response']['items'][0]['id']
      return owner_id

# Поиск фото по номеру аккаунта
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

# Работа с Яндексом 
class YaUploader:
  API_BASE_URL = "https://cloud-api.yandex.net:443"

  def __init__(self, token: str):
    self.token = token
    self.headers = {
      'Authorization': self.token
    }

# Создание новой папки
  def new_folder(self):
    name_folder = input(f'Как назвать папку? ')  
    req = requests.put(self.API_BASE_URL + '/v1/disk/resources?path=' + name_folder, headers=self.headers)
    # print(req)
    if req.status_code == 409:
      name_folder = name_folder + '(1)'
      req = requests.put(self.API_BASE_URL + '/v1/disk/resources?path=' + name_folder, headers=self.headers)
      print(f'Такая папка уже существует, документы будут загружены в папку {name_folder}')
    return name_folder

# Метод для загрузки файла по ссылке в папку Яндекс диска
  def upload(self, name_folder, name_file, path_to_file: str):
    name_folder_file = f'{name_folder}/{name_file}.jpeg'
    params = {
      'path': name_folder_file,
      'url' : path_to_file
    }
    requests.post(self.API_BASE_URL + '/v1/disk/resources/upload', 
    params=params, headers=self.headers)


if __name__ == "__main__":

  def VK_seach_photo_Yandex_upload():

# Получение ТОКЕНА. Если нет прикрепленного файла, используем ручной ввод.
    # with open('token_VK.txt', 'r') as file_object:
    #     token_VK = file_object.read().strip()
    token_VK = input('Введите свой ТОКЕН для ВК ')
    # with open('token_yandex.txt', 'r') as file_object:
    #     token_yandex = file_object.read().strip()
    token_yandex = input('Введите свой ТОКЕН для Яндекс Диска ')

   
# Работа по поиску фото профиля
    vk_client = VkUser(token_VK, '5.131')  
    user_ids = input('Введите id или имя аккаунта, чьи фото мы копируем: ')
    if user_ids.isdigit() == True:
      owner_id = int(user_ids)
    else:
      owner_id = vk_client.search_id(user_ids)
    
    print(f'Ищем фото аккаунта с id {owner_id}')
    photos_json = vk_client.search_photos(owner_id)
    photos_count = len(photos_json)
    # pprint(photos_json)

# Запрашиваю количество фоток для скачивания
    print(f'У аккаунта {owner_id} в профиле {photos_count} фотографий')
    photos_count_need = int(input('Сколько фотографий мы хотим скопировать: '))

    if photos_count_need < photos_count:
      photos_count = photos_count_need
    else:
      print('Скопируем сколько есть, больше никак')
    i = 0
# Создаю новый json по образцу
    new_json = []
    while i < photos_count:
      photos_dict = {}
      likes = photos_json[i]['likes']['count']

# Если лайки совпадают, то мы добавляем дату
      for x in new_json:
        if likes == x['file name']:
          likes = str(photos_json[i]['likes']['count']) + '.' + str(photos_json[i]['date'])
      size_len = len(photos_json[i]['sizes']) - 1 
      size = photos_json[i]['sizes'][size_len]
      photos_dict['file name'] = likes
      photos_dict['size'] = size
      new_json.append(photos_dict)
      i += 1
      
# При необходимости можем посмотреть список фотографий и информацию по размеру:
  # pprint(new_json)

# Работа по загрузке фото на Яндекс Диск
    uploader = YaUploader(token_yandex)  
    name_folder = uploader.new_folder()

# Загружаю фото поочереди по ссылке из созданного json файла
    x = 0
    while x < photos_count:
      name_file = new_json[x]['file name']
      path_to_file = new_json[x]['size']['url']
      uploader.upload(name_folder, name_file, path_to_file)
      x += 1
      print(f'Файл {name_file} загружен')
    print('ГОТОВО, Спасибо за внимание!')

# Вызов функции
  VK_seach_photo_Yandex_upload()

