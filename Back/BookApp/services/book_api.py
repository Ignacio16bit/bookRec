from django.conf import settings
import requests

def id_books(query):
    url=settings.OL_URL
    params={
        'q': query,
        'limit':1,
        'fields': 'key,author_name,subject'
    }

    try:
        response = requests.get(url,params=params, timeout=30)
        
        response.raise_for_status()
        data = response.json()
        return data

        if response.status_code==400:
            print(f'{query}: Libro no encontrado')
            return None

        elif response.status_code == 503:
            print('Open Library no parece estar disponible')
            return None

    except requests.exceptions.RequestException as e:
        print(f'Error en la API: {e}')
        return None
