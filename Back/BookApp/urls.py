from .views import BookView
from django.urls import path

urlpatterns=[
    path('recommend/', BookView.as_view(), name='book_search')
]