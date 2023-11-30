from django.db import models


MAX_LENGTH = 100


class Card(models.Model):
    name = models.CharField('Имя', max_length=MAX_LENGTH)
    last_name = models.CharField('Фамилия', max_length=MAX_LENGTH)

    class Meta:
        verbose_name = 'Карточка'

    def __str__(self):
        return self.name
