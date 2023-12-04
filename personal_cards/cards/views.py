from django.shortcuts import render

from .forms import CardForm
from .models import Attribute


def index(request):
    extra = Attribute.objects.all()
    form = CardForm(request.POST or None, extra=extra)
    if request.method == 'POST':
        form = CardForm(request.POST or None, request.FILES, extra=extra)
        if form.is_valid():
            for key, value in form.extra_fields():
                print('{} - {}'.format(key, value))
            print(form.cleaned_data)
            # print('Форма сохранена')
    context = {
        'form': form,
    }
    return render(
        request, 'index.html', context)
