from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Birthday(models.Model):
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=20,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        help_text='Необязательное поле',
        max_length=20,
    )
    birthday = models.DateField(
        verbose_name='Дата рождения',
    )
    price = models.IntegerField(
        verbose_name='Цена',
        help_text='Рекомендованная розничная цена',
        validators=[MinValueValidator(10), MaxValueValidator(100)],
    )    
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        null=True,
    )
