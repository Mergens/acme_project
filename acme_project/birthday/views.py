# birthday/views.py
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView, DetailView,
)
from django.urls import reverse_lazy

# Импортируем класс BirthdayForm, чтобы создать экземпляр формы.
from .forms import BirthdayForm
# Импортируем из utils.py функцию для подсчёта дней.
from .utils import calculate_birthday_countdown
from .models import Birthday


class BirthdayDetailView(DetailView):
    model = Birthday
    template_name_suffix = '_detail'


class BirthdayMixin:
    model = Birthday
    form_class = BirthdayForm
    template_name = 'birthday/birthday.html'
    success_url = reverse_lazy('birthday:list')


class BirthdayUpdateView(BirthdayMixin, UpdateView):
    pass
    # model = Birthday
    # form_class = BirthdayForm
    # template_name = 'birthday/birthday.html'
    # success_url = reverse_lazy('birthday:list')


class BirthdayCreateView(CreateView):
    pass
    # Указываем модель, с которой работает CBV...
    # model = Birthday
    # Этот класс сам может создать форму на основе модели!
    # Нет необходимости отдельно создавать форму через ModelForm.
    # Указываем поля, которые должны быть в форме:
    # fields = '__all__'

    # Применим эту полезную возможность и подключим форму BirthdayForm
    # к классу BirthdayCreateView: для этого вместо атрибута fields нужно
    # указать атрибут form_class; значением этого атрибута будет BirthdayForm.
    # Указываем имя формы:
    # form_class = BirthdayForm
    # Явным образом указываем шаблон:
    # template_name = 'birthday/birthday.html'
    # Указываем namespace:name страницы, куда будет перенаправлен пользователь
    # после создания объекта:
    # success_url = reverse_lazy('birthday:list')


def birthday(request, pk=None):
    # Если в запросе указан pk (если получен запрос на редактирование объекта):
    if pk is not None:
        # Получаем объект модели или выбрасываем 404 ошибку.
        instance = get_object_or_404(Birthday, pk=pk)
    # Если в запросе не указан pk
    # (если получен запрос к странице создания записи):
    else:
        # Связывать форму с объектом не нужно, установим значение None.
        instance = None
    # Если есть GET-параметры — передаём их в форму:
    form = BirthdayForm(
        request.POST or None,
        files=request.FILES or None,
        instance=instance,
        )
    # Форму с переданным в неё объектом request.GET
    # записываем в словарь контекста...
    # ...и отправляем в шаблон.
    context = {'form': form}
    if form.is_valid():
        form.save()
        # ...вызовем функцию подсчёта дней:
        birthday_countdown = calculate_birthday_countdown(
            # ...и передаём в неё дату из словаря cleaned_data.
            form.cleaned_data['birthday']
        )
        # Обновляем словарь контекста: добавляем в него новый элемент.
        context.update({'birthday_countdown': birthday_countdown})
    return render(request, 'birthday/birthday.html', context)


# Наследуем класс от встроенного ListView:
class BirthdayListView(ListView):
    # Указываем модель, с которой работает CBV...
    model = Birthday
    # ...сортировку, которая будет применена при выводе списка объектов:
    ordering = 'id'
    # ...и даже настройки пагинации:
    paginate_by = 10


def birthday_list(request):
    # Получаем все объекты модели Birthday из БД.
    birthdays = Birthday.objects.all().order_by('id')
    # Создаём объект пагинатора с количеством 10 записей на страниц
    paginator = Paginator(birthdays, 10)
    # Получаем из запроса значение параметра page.
    page_number = request.GET.get('page')
    # Получаем запрошенную страницу пагинатора.
    # Если параметра page нет в запросе или его значение не приводится к числу,
    # вернётся первая страница.
    page_obj = paginator.get_page(page_number)

    # Передаём их в контекст шаблона.
    context = {'page_obj': page_obj}
    return render(request, 'birthday/birthday_list.html', context)


class BirthdayDeleteView(DeleteView):
    model = Birthday
    success_url = reverse_lazy('birthday:list')


def delete_birthday(request, pk):
    # Получаем объект модели или выбрасываем 404 ошибку.
    instance = get_object_or_404(Birthday, pk=pk)
    # В форму передаём только объект модели;
    # передавать в форму параметры запроса не нужно.
    form = BirthdayForm(instance=instance)
    context = {'form': form}
    # Если был получен POST-запрос...
    if request.method == 'POST':
        # ...удаляем объект:
        instance.delete()
        # ...и переадресовываем пользователя на страницу со списком записей.
        return redirect('birthday:list')
    # Если был получен GET-запрос — отображаем форму.
    return render(request, 'birthday/birthday.html', context)


def edit_birthday(request, pk):
    # Находим запрошенный объект для редактирования по первичному ключу
    # или возвращаем 404 ошибку, если такого объекта нет.
    instance = get_object_or_404(Birthday, pk=pk)
    # Связываем форму с найденным объектом: передаём его в аргумент instance.
    form = BirthdayForm(request.POST or None, instance=instance)
    # Всё остальное без изменений.
    context = {'form': form}
    # Сохраняем данные, полученные из формы, и отправляем ответ:
    if form.is_valid():
        form.save()
        birthday_countdown = calculate_birthday_countdown(
            form.cleaned_data['birthday']
        )
        context.update({'birthday_countdown': birthday_countdown})
    return render(request, 'birthday/birthday.html', context)
