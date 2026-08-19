from django.conf import settings
import requests

def id_books(query):
    url=settings.OL_URL
    headers = {
        "User-Agent": "BookRec/0.1 (ignaciopux@gmail.com)"
    }
    params={
        'q': query,
        'limit':5,
        'fields': 'title,key,author_name,subject'
    }

    try:
        response = requests.get(url,params=params, headers=headers ,timeout=30)

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

        docs = response.json().get('docs',[])

        for book in docs:
            subject = book.get('subject',[])

            if len(subject)>=3:
                return book
            else:
                return None

    except requests.exceptions.RequestException as e:
        print(f'Error en la API: {e}')
        return None

def get_books_by_subjects(subjects):
    if not subjects:
        return None

    subject_query = ' OR '.join(subjects)
    query = f'subject:({subject_query})'
    headers = {
        "User-Agent": "BookRec/0.1 (ignaciopux@gmail.com)"
    }
    url = settings.OL_URL
    params = {
        'q':query,
        'limit':15,
        'fields': 'title,key,author_name,subject'
        }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=30)

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

        return response.json().get('docs',[])
    
    except requests.exceptions.RequestException as e:
        print(f'Error al recuperar libros: {e}')
        return []