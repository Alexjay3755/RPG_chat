from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField

class User(AbstractUser):
    code = models.CharField(max_length=10, null=True, blank=True)


class Post(models.Model):

    tanks = 'TA'
    healers = 'HL'
    dd = 'DD'
    merchants = 'MC'
    guildmasters = 'GM'
    questgivers = 'QG'
    blacksmiths = 'BS'
    tanners = 'TN'
    potionmakers = 'PM'
    spellmasters = 'SM'

    options = [
        (tanks, 'Танки'),
        (healers, 'Хилы'),
        (dd, 'ДД'),
        (merchants, 'Торговцы'),
        (guildmasters, 'Гилдмастеры'),
        (questgivers, 'Квестгиверы'),
        (blacksmiths, 'Кузнецы'),
        (tanners, 'Кожевники'),
        (potionmakers, 'Зельевары'),
        (spellmasters, 'Мастера заклинаний'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = RichTextUploadingField()
    category = models.CharField(max_length=2, choices=options, default=tanks)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.content



