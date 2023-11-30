from django.shortcuts import render

from .forms import CardForm


def index(request):
    template = 'index.html'
    context = {'form': CardForm}
    return render(request, template, context)
