# birthday/forms.py
from django import forms


# birthday/forms.py
class BirthdayForm(forms.Form):
    first_name = forms.CharField(
        label='Имя',
        max_length=20
    )
    last_name = forms.CharField(
        label='Фамилия',
        required=False,
        help_text='Необязательное поле'
    )
    birthday = forms.DateField(
        label='Дата рождения',
        # Указываем, что виджет для ввода даты должен быть с типом date.
        widget=forms.DateInput(attrs={'type': 'date'})        
    )

    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'cols': 100, 'rows': 10}),
        label='Описание: ')