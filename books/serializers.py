
from rest_framework import serializers
from .models import Book, Favorite


# --------------------------------
# BOOK SERIALIZER
# --------------------------------

class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book

        fields = [
            'id',
            'external_id',
            'title',
            'author',
            'description',
            'isbn',
            'category',
            'cover_image',
            'created_at',
        ]

        read_only_fields = [
            'id',
            'created_at',
        ]


# --------------------------------
# FAVORITE SERIALIZER
# --------------------------------

class FavoriteSerializer(serializers.ModelSerializer):

    user = serializers.ReadOnlyField(
        source='user.username'
    )

    book_title = serializers.CharField(
        source='book.title',
        read_only=True
    )

    class Meta:
        model = Favorite

        fields = [
            'id',
            'user',
            'book',
            'book_title',
            'created_at',
        ]

        read_only_fields = [
            'id',
            'user',
            'created_at',
        ]

    def validate_book(self, value):

        request = self.context.get('request')

        if request and request.user.is_authenticated:

            already_exists = Favorite.objects.filter(
                user=request.user,
                book=value
            ).exists()

            if already_exists:
                raise serializers.ValidationError(
                    "This book is already in your favorites."
                )

        return value
