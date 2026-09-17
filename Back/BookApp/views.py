from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .services.book_api import id_books, get_books_by_subjects
from .services.recommend import vectorizer

class BookView(APIView):
    def get(self, request):
        query = request.query_params.get('q')

        if not query:
            return Response(
                {'error':'No se ha recibido parámetro de búsqueda'},
                status = status.HTTP_400_BAD_REQUEST
            )

        print("\n Buscando libro por título...")
        print(f"- Consulta: '{query}'")

        target_book = id_books(query)

        if not target_book:
            return Response(
                {'error':'Libro no encontrado'},
                status = status.HTTP_404_NOT_FOUND
            )

        print(f'Libro devuelto: {target_book}')

        target_subjects = target_book.get('subject',[])[:10]
        print(f"- Total de temas: {len(target_subjects)}")
        print(f"- Lista de temas: {target_subjects}")

        if not target_subjects:
            return Response(
                {'error':'No se encontraron obras con los parámetros necesarios. Pruebe con el título en inglés o introduciendo el nombre del autor.'},
                status = status.HTTP_404_NOT_FOUND
            )

        candidates = get_books_by_subjects(target_subjects)

        if not candidates:
            return Response(
                {'error': 'No hay libros coincidentes con los temas'},
                status = status.HTTP_404_NOT_FOUND
            )

        #Extraer las listas de géneros para no pasar diccionarios
        candidates_subjects = [book.get('subject', []) for book in candidates]

        candidate_books = [book.get('title', []) for book in candidates]
        print(f'Libros con temas coincidentes: {candidate_books}')

        sim = vectorizer(target_subjects, candidates_subjects)

        if sim is None:
            return Response(
                {'error':'Error al procesar la solicitud'},
                status = status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        #Formateado de datos
        formatted_rec = []
        for candidate, score in zip(candidates, sim):
            formatted_rec.append({
                'title': candidate.get('title', 'Sin título'),
                'author': candidate.get('author_name'),
                'cover_id':candidate.get('cover_i'),
                'similarity':round(float(score),2)
            })

        formatted_rec.sort(key=lambda x: x['similarity'], reverse=True)

        return Response({
            'input_book':{
                'title':target_book.get('title'),
                'author':target_book.get('author_name', []),
                'subjects':target_subjects
            },
            'recommendations':formatted_rec,
            'total': len(formatted_rec)
        })