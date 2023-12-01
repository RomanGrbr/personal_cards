from django.shortcuts import render
from django.forms import formset_factory, inlineformset_factory

from .forms import CardForm, AttrValueForm, PersonForm


# def index(request):
#     template = 'index.html'
#     context = {'form': CardForm}
#     return render(request, template, context)

def index(request):
    # form = PersonForm()
    extra_forms = 1
    AttrValueFormSet = formset_factory(AttrValueForm, extra=extra_forms, max_num=20)
    # forms = [PersonForm, AttrValueFormSet]
    if request.method == 'POST':
        print(request.POST)
        if 'additems' in request.POST and request.POST['additems'] == 'true':
            formset_dictionary_copy = request.POST.copy()
            formset_dictionary_copy['form-TOTAL_FORMS'] = (
                    int(formset_dictionary_copy['form-TOTAL_FORMS']) + extra_forms)
            formset = AttrValueFormSet(formset_dictionary_copy)
        else:
            formset = AttrValueFormSet(request.POST)
            if formset.is_valid():
                print('Форма сохранена')
    else:
        formset = AttrValueFormSet(
            initial=[{'name': 1, 'size': 'm', 'amount': 1}])
    context = {
        'formset': [PersonForm, formset],
        # 'form': form
    }
    return render(
        request, 'index.html', context)
