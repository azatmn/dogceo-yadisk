import requests
from tqdm import tqdm
import json

class _DogCeo:
    def __init__(self, breed):
        self.breed = breed

    def _input_accuracy(self):
        url = 'https://dog.ceo/api/breeds/list/all'
        response = requests.get(url).json()
        return self.breed in response['message']

    def _check_sub_breeds(self):
        url = f'https://dog.ceo/api/breed/{self.breed}/list'
        response = requests.get(url).json()
        return response['message']

    def search_photos(self):
        if not self._input_accuracy():
            print('Breed is not recognized')
            exit()

        sub_breeds = self._check_sub_breeds()
        if sub_breeds:
            photos = {}
            print('\nSearch Photo')
            for sub_breed in tqdm(sub_breeds):
                url = f'https://dog.ceo/api/breed/{self.breed}/{sub_breed}/images/random'
                response = requests.get(url).json()
                photos[f'{self.breed}-{sub_breed}'] = response['message']
            return photos

        else:
            url = f'https://dog.ceo/api/breed/{self.breed}/images/random'
            response = requests.get(url).json()
            return {f'{self.breed}': response['message']}



class YaDisk:
    token = 'ВВЕДИТЕ ВАШ ТОКЕН ЯНДЕКС ДИСКА'
    group = 'FPY-130'
    def __init__(self, breed):
        self.breed = breed.lower()

    def _call_dogceo(self):
        return _DogCeo(self.breed).search_photos()

    def _create_folder(self, folder_name = ''):
        url_create_folder = 'https://cloud-api.yandex.net/v1/disk/resources'
        params = {'path': str(self.group + '/' + folder_name)}
        headers = {'Authorization': f'OAuth {self.token}'}
        requests.put(url_create_folder, params=params, headers=headers)

    def _upload_photo(self, photos):
        url_photo_upload = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = {'Authorization': f'OAuth {self.token}'}
        print('\nUpload Photo')
        for photo in tqdm(photos):
            params = {
                'path': f'{self.group}/{self.breed}/{photo}.{photos[photo].split("/")[-1][:-4]}',
                'url': photos[photo],
                'disable_redirects': 'false'
            }
            requests.post(url_photo_upload, params=params, headers=headers)

    def _file_result_json(self, photos):
        result_json = json.dumps(photos, ensure_ascii=False)
        url_upload_link = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        params = {
            'path': f'{self.group}/{self.breed}/result.json',
            'overwrite': 'true'
        }
        headers = {'Authorization': f'OAuth {self.token}'}
        response_upload_link = requests.get(url_upload_link, params=params, headers=headers)
        upload_url = response_upload_link.json()['href']
        requests.put(upload_url, data=result_json.encode("utf-8"))

    def yadisk_upload_photo(self):
        photos = self._call_dogceo()
        self._create_folder()
        self._create_folder(self.breed)
        self._upload_photo(photos)
        self._file_result_json(photos)


if __name__ == '__main__':
    breed = input('Enter the breed: ')
    dog = YaDisk(breed)
    dog.yadisk_upload_photo()