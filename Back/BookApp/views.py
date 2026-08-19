from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .services.book_api import id_books, get_books_by_subjects

# Create your views here.

class BookView(APIView):
    def get(self, request):
        query = request.query_params.get('q')

        if not query:
            return Response(
                {'error':'No se ha recibido parámetro de búsqueda'},
                status = status.HTTP_400_BAD_REQUEST
            )

        print("\n Buscando libro por título...")
        print(f"   → Consulta: '{query}'")

        data = id_books(query)

        docs = data.get('docs',[])
        if not docs:
            return Response(
                {'error':'Libro no encontrado'},
                status = status.HTTP_404_NOT_FOUND
            )
        book = docs[0]

        print(f'Libro devuelto: {book}')

        subjects = book.get('subject',[])
        subjects = subjects[:10] #Limito a 10 para reducir carga en
        print(f"   → Total de temas: {len(subjects)}")
        print(f"   → Lista de temas: {subjects}")

        if not subjects:
            print('No hay temas asociados al libro')

        candidates = get_books_by_subjects(subjects)

        return Response(
            {
                'input_book': book,
                'candidates':candidates
            },
            status=status.HTTP_200_OK
        )