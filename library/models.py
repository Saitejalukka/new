from django.db import models
from django.conf import settings
from books.models import Book


class Favorite(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="favorites"
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="favorited_by"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "book"],
                name="unique_favorite"
            )
        ]

    def __str__(self):
        return f"{self.user} - {self.book.title}"


class SavedBook(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="saved_books"
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="saved_by"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "book"],
                name="unique_saved_book"
            )
        ]

    def __str__(self):
        return f"{self.user} - {self.book.title}"


class ReadingList(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reading_lists"
    )
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    books = models.ManyToManyField(
        Book,
        through="ReadingListItem",
        related_name="reading_lists"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ReadingListItem(models.Model):
    reading_list = models.ForeignKey(
        ReadingList,
        on_delete=models.CASCADE,
        related_name="items"
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="reading_list_items"
    )
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["reading_list", "book"],
                name="unique_reading_list_book"
            )
        ]

    def __str__(self):
        return f"{self.reading_list.name} - {self.book.title}"