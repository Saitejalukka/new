from django.db import models
from django.conf import settings


class Book(models.Model):

    external_id = models.CharField(
        max_length=200,
        unique=True
    )
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    isbn = models.CharField(
    max_length=20,
    blank=True
    )
    category = models.CharField(
    max_length=100,
    blank=True
    )
    cover_image = models.URLField(blank=True)
    created_at = models.DateTimeField(
    auto_now_add=True
    )
    def __str__(self):
        return self.title
class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='book_favorites')
    book = models.ForeignKey(Book, on_delete=models.CASCADE,related_name='book_favorites')
    created_at = models.DateTimeField(auto_now_add=True)

class Meta:
    constraints = [
        models.UniqueConstraint(
            fields=['user', 'book'],
            name='unique_user_favorite'
            )
        ]

    def __str__(self):
        return f"{self.user.username} favorited {self.book.title}"