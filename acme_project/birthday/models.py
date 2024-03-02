from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from .validators import real_age


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
        verbose_name='Дата рождения', validators=(real_age,)
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
    image = models.ImageField(
        verbose_name='Фото',
        upload_to='birthdays_images',
        blank=True,
    )
