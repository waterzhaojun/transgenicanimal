from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect

from django.views import generic, View
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.db.models import Q

from .models import TransgenicAnimalLog, TransgenicMouseBreeding
from .forms import AnimalMateForm, AnimalInfoForm
from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required # to limit some function only for login user

from . import utils
import numpy as np
from datetime import datetime
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

        animals = TransgenicAnimalLog.objects.filter(~Q(cageid = 'terminated'))
        mates = TransgenicMouseBreeding.objects.filter(inprocess = True)

        context['animals'] = sorted(animals.order_by('cageid'), key = lambda t: t.strain)
        context['mates'] = mates.order_by('cageid')
        context['info'] = {
            'num_of_animals': animals.count(),
            'num_of_unsac_animals': animals.filter(~Q(schedule__purpose = 'terminate')).count(),
            'num_of_total_cages': animals.distinct('cageid').count(),
            'num_of_mating_cages': mates.distinct('cageid').count(),
            'num_of_mating_cages_after_sac': mates.filter(~Q(mother__schedule__purpose = 'terminate') or ~Q(father__schedule__purpose = 'terminate')).count(),
            'num_of_unsac_cages': animals.filter(~Q(schedule__purpose = 'terminate')).distinct('cageid').count()
            
        }
        print(mates.filter(~Q(mother__schedule__purpose = 'terminate') or ~Q(father__schedule__purpose = 'terminate')))
        
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
        if 'animalid' in kwargs.keys():
            animalid = kwargs['animalid']
        else:
            animalid = dict(request.GET.lists())['animalid'][0]
            print(request.GET.lists())
            print(animalid)

        animal = TransgenicAnimalLog.objects.filter(animalid = animalid)[0]
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


"""class AnimalCreate(generic.CreateView):
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
"""
class MateInfo(generic.DetailView): # have to use updateview instead of detailview as detailview doesn't output a form
    model = TransgenicMouseBreeding
    template_name = 'transgenicanimal/mateinfo.html'
   
class CageInfo(generic.DetailView):
    model = TransgenicAnimalLog
    template_name = 'transgenicanimal/cageinfo.html'
    #queryset = TransgenicAnimalLog.objects.filter(~Q(cageid = 'terminated'))
    def get(self, request, **kwargs):
        cageid = kwargs['cageid']
        animals = sorted(TransgenicAnimalLog.objects.filter(cageid = cageid), key = lambda t: t.animalid)
        context = {
            'animals': animals,
            'cageid': cageid
        }
        return render(request, self.template_name, context)


@login_required
def terminate(request, animalid):
    TransgenicAnimalLog.objects.filter(animalid = animalid).update(cageid='terminated')
    return HttpResponseRedirect(reverse('transgenicanimal')) # reverse by this url name.

@login_required      
def givebirth(request, mateid):
    day = datetime.today() - timedelta(days=int(request.POST.get('days')))
    TransgenicMouseBreeding.objects.filter(mateid = mateid).update(birthday=day)
    return HttpResponseRedirect(reverse('transgenicanimal'))
    
@login_required
def wean(request, mateid):
    malenum = int(request.POST.get('malenum'))
    femalenum = int(request.POST.get('femalenum'))
    malecage = request.POST.get('malecage')
    femalecage = request.POST.get('femalecage')
    keepmate = request.POST.get('keepmate') == 'yes'

    mate = TransgenicMouseBreeding.objects.filter(mateid = mateid).first()
    allnum = malenum + femalenum
    genderlist = np.concatenate([np.repeat('M', malenum), np.repeat('F', femalenum)])
    cagelist = np.concatenate([np.repeat(malecage, malenum), np.repeat(femalecage, femalenum)])
    mateid = getattr(mate, 'mateid')
    father = getattr(mate, 'father')
    mother = getattr(mate, 'mother')
    birthday = getattr(mate, 'birthday')
    generation = request.POST.get('generation')

    for i in range(allnum):
        aid = utils.namekid(
            [getattr(father, 'animalid'), getattr(mother, 'animalid')], 
            birthday, mateid, i
        )
        print(aid)
        print(genderlist[i])
        print(cagelist[i])
        TransgenicAnimalLog.objects.create(
            animalid=aid,
            cageid=cagelist[i],
            dob=birthday,
            gender=genderlist[i],
            birth_mate=mate,
            generation=generation,
        )

    mate.weaning_date = datetime.today()
    mate.inprocess = False
    mate.save()

    if keepmate:
        allmateid = [int(x[1:]) for x in list(TransgenicMouseBreeding.objects.values_list('mateid', flat = True))]
        # use values_list instead of values can remove keys
        allmateid.sort()
        newmateid = 'M' + '%04d'% (allmateid[-1]+1)
        print(newmateid)
        TransgenicMouseBreeding.objects.create(
            mateid=newmateid,
            cageid=getattr(mate, 'cageid'),
            father=father,
            mother=mother,
            pair_date=getattr(mate,'pair_date'),
            inprocess=True
        )
    
    return HttpResponseRedirect(reverse('transgenicanimal'))

@login_required
def resetbirth(request, mateid):
    TransgenicMouseBreeding.objects.filter(mateid = mateid).update(birthday=None)
    return HttpResponseRedirect(reverse('transgenicanimal')) # reverse by this url name.

@login_required
def stopmate(request, mateid):
    TransgenicMouseBreeding.objects.filter(mateid = mateid).update(inprocess=False)
    return HttpResponseRedirect(reverse('transgenicanimal')) # reverse by this url name.

@login_required
def move(request, animalid):
    TransgenicAnimalLog.objects.filter(animalid = animalid).update(cageid=request.POST.get('cageid'))
    return HttpResponseRedirect(reverse('transgenicanimal')) 

@login_required
def schedule(request, animalid):
    purpose = request.POST.get('purpose')
    username = request.user.username
    animal = TransgenicAnimalLog.objects.filter(animalid = animalid).first()
    if purpose == 'cancel_terminate':
        animal.schedule = None
    else:
        animal.schedule = {'purpose': purpose, 'person': username}
    animal.save()
    return HttpResponseRedirect(reverse('transgenicanimal')) 

@login_required
def createmate(request, cageid):
    animals = TransgenicAnimalLog.objects.filter(cageid = cageid)
    animals_m = [x for x in animals if getattr(x, 'gender') == 'M']
    animals_f = [x for x in animals if getattr(x, 'gender') == 'F']
    if len(animals_m) == 1 and len(animals_f) > 0:
        allmateid = [int(x[1:]) for x in list(TransgenicMouseBreeding.objects.values_list('mateid', flat = True))]
        # use values_list instead of values can remove keys
        allmateid.sort()
        father = animals_m[0]
        for i in range(len(animals_f)):
            mother = animals_f[i]
            TransgenicMouseBreeding.objects.create(
                mateid='M' + '%04d'% (allmateid[-1]+1+i),
                cageid=cageid,
                father=father,
                mother=mother,
                pair_date=datetime.today(),
                inprocess=True
            )
    
    return HttpResponseRedirect(reverse('transgenicanimal')) 