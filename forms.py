from django import forms
from .models import TransgenicAnimalLog, TransgenicMouseBreeding
from django.db.models import Q

# class AnimalInfoForm(forms.ModelForm):
#     class Meta:
#         model=TransgenicAnimalLog
#         fields = ['animalid', 'cageid', 'ear_punch']

    # def form_valid(self, form):
    #     print(form)
    #     return super().form_valid(form)

class AnimalMateForm(forms.ModelForm):
    class Meta:
        model=TransgenicMouseBreeding
        # animals = TransgenicAnimalLog
        fields = ('cageid',)#'__all__' #('mateid', 'cageid', 'father', 'mother', 'pair_date', 'note')  # use '__all__' to use all field from the model
        # override the default widget for each field
        # self.form.fields['father'].queryset = TransgenicAnimalLog.objects.filter(~Q(cageid = 'terminated'))
        # form.rate.queryset = Rate.objects.filter(company_id=the_company.id)
        widgets = {'pair_date': forms.SelectDateWidget,
        }

class AnimalInfoForm(forms.ModelForm):
    class Meta:
        model=TransgenicAnimalLog
        fields = '__all__' 
        widgets = {
            'dob': forms.SelectDateWidget(years = [2016, 2017, 2018, 2019, 2020, 2021, 2022]),
        }

        def clean_jsonfield(self):
            jdata = self.cleaned_data['genotype']
            try:
                json_data = json.loads(jdata) #loads string as json
                #validate json_data
            except:
                raise forms.ValidationError("Invalid data in jsonfield")
                #if json data not valid:
                #raise forms.ValidationError("Invalid data in jsonfield")
            return jdata
