# birthday/forms.py
from django.forms import ModelForm
from django import forms
# Импортируем класс модели Birthday.
from .models import Birthday


# Для использования формы с моделями меняем класс на forms.ModelForm.
class BirthdayForm(ModelForm):
    # Все настройки задаём в подклассе Meta.
    class Meta:
        # Указываем модель, на основе которой должна строиться форма.
        model = Birthday
        # Указываем, что надо отобразить все поля.
        fields = '__all__'
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'cols': 100, 'rows': 10}),
        }
