from django.db import models

from django.contrib.auth.models import User
from django.urls import reverse

class Board(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE, related_name='user_boards')

    title = models.CharField(max_length=50)
    content = models.TextField()
    photo = models.ImageField(upload_to='photos/%Y/%m/%d', default='photos/no_image.png')

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    STATUS_CHOICES = (
        ('normal', '보이게'),
        ('banned', '안보이게'),
    )
    status = models.CharField(max_length=6, choices=STATUS_CHOICES, default='normal')

    class Meta:
        ordering = ['-updated']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('board:detail', args=[str(self.id)])
