from django.conf import settings
import requests

def id_books(query):
    url=settings.OL_URL
    headers = {
        "User-Agent": "BookRec/0.1 (ignaciopux@gmail.com)"
    }
    params={
        'q': query,
        'limit':1,
        'fields': 'key,author_name,subject',
        'headers': headers
    }

    try:
        response = requests.get(url,params=params, timeout=30)

        if response.status_code==400:
            print(f'{query}: Datos inválidos para la búsqueda')
            return None
        
        elif response.status_code==404:
            print(f'{query}: Libro no encontrado')
            return None

        elif response.status_code == 503:
            print('Open Library no parece estar disponible')
            return None

        elif response.status_code != 200:
            print(f'Error HTTP: {response.status_code}')
            return None

        data = response.json()
        return data

    except requests.exceptions.RequestException as e:
        print(f'Error en la API: {e}')
        return None
