from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect

from django.views import generic, View
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.db.models import Q

from .models import TransgenicAnimalLog, TransgenicMouseBreeding
from .forms import AnimalMateForm, AnimalInfoForm
from datetime import datetime, timedelta

# Create your views here.

# from django.template import loader # use shortcuts instead of loader

# Create your views here.
class index(generic.ListView):
    template_name = 'transgenicanimal/index.html'   # if use ListView class, default template_name is _list.html. So you have to revise it.
    queryset = TransgenicAnimalLog.objects.filter(~Q(cageid = 'terminated'))   # default output variable. In template, use object_list to refer to this.
    # the default output to tmplate is object_list
    def get_context_data(self, **kwargs):
        # queryset is the default output, besides that, you can use get_context_data to add more in the dict.
        context = super(index, self).get_context_data(**kwargs)
        context['animals'] = sorted(TransgenicAnimalLog.objects.filter(~Q(cageid = 'terminated')), key = lambda t: t.strain)
        context['mates'] = TransgenicMouseBreeding.objects.filter(inprocess = True)
        return context
    # context is like a big box send to template, in this box we have object_list which is a default variable if you just define model =...
    # Now we add 'animals' and 'mates' in the box. So in template, we can use animals and mates.

class AnimalInfo(View):
    # model = TransgenicAnimalLog
    template_name = 'transgenicanimal/animalinfo.html'

    # def get_object(self):  # it is another option instead of queryset
    #     id_ = self.kwargs.get('id')
    #     return get_object_or_404(TransgenicAnimalLog, id=id_)
    def get(self, request, **kwargs):
        animal = TransgenicAnimalLog.objects.filter(animalid = kwargs['pk'])[0]
        mate = animal.birth_mate
        context = {'animal': animal}
        # print(getattr(mate.father, 'animalid'))
        try:
            context['fatherid'] = getattr(mate.father, 'animalid')
        except:
            context['fatherid'] = None
        try:
            context['motherid'] = getattr(mate.mother, 'animalid')
        except:
            context['motherid'] = None        

        return render(request, self.template_name, context)
    # def get_context_data(self, **k)


class AnimalCreate(generic.CreateView):
    form_class = AnimalInfoForm
    model = TransgenicAnimalLog
    template_name = 'transgenicanimal/create.html'
    queryset = TransgenicAnimalLog.objects.filter(~Q(cageid = 'terminated'))


class MateCreate(generic.CreateView):
    form_class = AnimalMateForm  #it is not form here. If use form, you need add fields. And the form field widget will be overrided.
    model = TransgenicMouseBreeding
    template_name = 'transgenicanimal/create.html'
    # fields = ['mateid', 'cageid', 'father', 'mother', 'pair_date', 'note']  # this is refered to class in forms.py. the format of the value is defined there.
    # queryset = TransgenicMouseBreeding.objects.filter(inprocess = True)

class MateInfo(generic.DetailView): # have to use updateview instead of detailview as detailview doesn't output a form
    model = TransgenicMouseBreeding
    template_name = 'transgenicanimal/mateinfo.html'
   



# following part is just for backup a function view writing method.
"""
def animalinfo(request, animalid):
    animal = TransgenicAnimalLog.objects.get(pk = animalid)
    context = {'animal': animal}
    return render(request, 'transgmice/animal_info.html', context)
    #return HttpResponse("<h2>info for animal " + animal.cageid + "</h2>")

def breeding(request):
    breedlist = TransgenicMouseBreeding.objects.all()
    context = {'breedlist': breedlist}
    return render(request, 'tr')
""" 

def terminate(request, animalid):
    TransgenicAnimalLog.objects.filter(animalid = animalid).update(cageid='terminated')
    return HttpResponseRedirect(reverse('transgenicanimal')) # reverse by this url name.
        
def givebirth(request, mateid):
    day = datetime.today() - timedelta(days=int(request.POST.get('days')))
    TransgenicMouseBreeding.objects.filter(mateid = mateid).update(birthday=day)
    return HttpResponseRedirect(reverse('transgenicanimal'))
    
