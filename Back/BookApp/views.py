from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .services.book_api import id_books
# Create your views here.
class BookView(APIView):
    def get(self, request):
        query = request.query_params.get('q')

        if not query:
            return Response(
                {'error':'No se ha recibido parámetro de búsqueda'},
                status = status.HTTP_400_BAD_REQUEST
            )

        result = id_books(query)
        print(f'Libro devuelto: {result}')

        if not result:
            return Response(
                {'error':'Libro no encontrado'},
                status = status.HTTP_404_NOT_FOUND
            )
        
        return Response(result, status=status.HTTP_200_OK)