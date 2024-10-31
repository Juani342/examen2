import urllib.request
import json


class API:
    def __init__(self, base_url):
        self.__base_url = base_url

    def fetch_records(self):
        try:
            with urllib.request.urlopen(self.__base_url) as response:
                data = response.read().decode('utf-8')
                return json.loads(data)
        except (urllib.error.HTTPError, urllib.error.URLError) as e:
            print(f"Error en la solicitud: {e}")
            return []