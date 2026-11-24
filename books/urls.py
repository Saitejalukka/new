
from django.urls import path

from .views import BookSearchView, book_list


urlpatterns = [

    path(
        '',
        book_list,
        name='book-list'
    ),

    path(
        'search/',
        BookSearchView.as_view(),
        name='book-search'
    ),

]
