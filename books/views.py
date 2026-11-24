
from django.shortcuts import render
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Book
from .serializers import BookSerializer


class BookSearchView(generics.ListAPIView):

    serializer_class = BookSerializer

    def get_queryset(self):

        queryset = Book.objects.all()

        search_query = self.request.query_params.get("q")

        if search_query:
            from django.db.models import Q

            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(author__icontains=search_query)
            )

        return queryset.distinct()


@api_view(['GET'])
def book_list(request):

    books = Book.objects.all()

    serializer = BookSerializer(
        books,
        many=True
    )

    return Response(serializer.data)
