# birthday/views.py
from django.shortcuts import render

# Импортируем класс BirthdayForm, чтобы создать экземпляр формы.
from .forms import BirthdayForm
# Импортируем из utils.py функцию для подсчёта дней.
from .utils import calculate_birthday_countdown


def birthday(request):
    # Если есть GET-параметры — передаём их в форму:
    form = BirthdayForm(request.GET or None)
    # Форму с переданным в неё объектом request.GET 
    # записываем в словарь контекста...   
    # ...и отправляем в шаблон. 
    context = {'form': form}
    if form.is_valid():
        # ...вызовем функцию подсчёта дней:
        birthday_countdown = calculate_birthday_countdown(
            # ...и передаём в неё дату из словаря cleaned_data.
            form.cleaned_data['birthday']
        )
        # Обновляем словарь контекста: добавляем в него новый элемент.
        context.update({'birthday_countdown': birthday_countdown})    
    
    return render(request, 'birthday/birthday.html', context) 