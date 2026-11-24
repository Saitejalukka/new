
from django.db import models
from django.conf import settings
from books.models import Book


class ReadingHistory(models.Model):

    STATUS_CHOICES = [
        ('WANT_TO_READ', 'Want to Read'),
        ('CURRENTLY_READING', 'Currently Reading'),
        ('COMPLETED', 'Completed'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reading_history'
    )

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='reading_histories'
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='WANT_TO_READ'
    )

    progress = models.PositiveSmallIntegerField(default=0)

    started_at = models.DateTimeField(
        null=True,
        blank=True
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'book'],
                name='unique_user_reading_book'
            ),
            models.CheckConstraint(
                condition=models.Q(progress__lte=100),
                name='reading_progress_max_100'
            )
        ]

        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.user} - {self.book.title}"
