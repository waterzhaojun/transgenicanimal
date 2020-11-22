from django import forms
from .models import TransgenicAnimalLog, TransgenicMouseBreeding, SurgTreatment
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
            #'gender': forms.ChoiceField(
            #    choices=[('M','M'),('F','F')])#, 
                #widget=forms.RadioSelect)
        }

        def clean_jsonfield(self): # I am not sure if I am using this set.
            jdata = self.cleaned_data['genotype']
            try:
                json_data = json.loads(jdata) #loads string as json
                #validate json_data
            except:
                raise forms.ValidationError("Invalid data in jsonfield")
                #if json data not valid:
                #raise forms.ValidationError("Invalid data in jsonfield")
            return jdata
    gender = forms.ChoiceField(
        choices=[('M','M'),('F','F')]
    )
    species = forms.ChoiceField(
        choices=[('mouse', 'mouse'), ('rat','rat')]
    )


class AavinjectForm(forms.ModelForm):

    # def __init__(self, *args, **kwargs): 这么写是不成功的，我决定不加animalid了。
    #     self.animalid = kwargs.pop('animalid')
    #     super(AavinjectForm, self).__init__(*args, **kwargs)

    aavlist = [
        ('0', 'AAV5.CAG.GCaMP6s.WPRE.SV40'), 
        ('1','AAV1.CAG.GCaMP6s.WPRE'),
        ('2','AAV5.GfaABC1D.cyto.GCaMP6f.SV40'),
        ('3','AAV-PHP.S CA6.6PP'),
        ('4','AAV2/5.GFAP.hM3D(Gq).mCherry (do not use this one)'),
        ('5','AAV5.GFAP.hM3D(Gq).mCherry'),
        ('6','pGP.AAV.syn.JGCaMP7s.WPRE'),
        ('7','AAV2/5-gfaABCD1-optoGq-EYFP'),
        ('8','AAV9.CAG.flex.GCaMP5s.WPRE.SV40'),
        ('9','PNS1.CAG.GCaMP6s'),
        ('10','PNS1.CAG.DIO.GCaMP6s'),
        ('11','pAAV.hSyn.hChR2(H134R).EYFP')
    ]
    inject_method_list = [
        ('0', 'superficial cortical injection'), 
        ('1','TG injection from contra lateral cortex'), 
        ('2','TG injection from ipsi lateral cortex'), 
        ('3','TG injection from nasal'),
        ('4','retro orbital injection'), 
        ('5','apply topically'),
        ('6','iv injection')
    ]
    inject_tool_list = [
        ('0','glass pipette'), 
        ('1','needle'), 
        ('2','insolin syringe')
    ]

    aav = forms.ChoiceField(choices = aavlist)
    inject_method = forms.ChoiceField(choices = inject_method_list)
    inject_volumn = forms.FloatField(
        label = 'Input volumn (ul). It is the total amount: '
    )
    inject_dose = forms.CharField(
        label = 'Input dose. It is the true amount (vg) like 1.00E12: ',
        required=False
    )
    depth_num_of_each_spot = forms.IntegerField(
        label = 'inject depth of each spot.',
        initial = 1,
        required = False
    )
    inject_tool = forms.ChoiceField(choices = inject_tool_list)
    
    class Meta:
        model = SurgTreatment
        fields = ('date','time','note','aav','inject_method',
            'inject_volumn','inject_dose','depth_num_of_each_spot','inject_tool'
        )
        widgets = {
            'date': forms.SelectDateWidget,
        }

    def clean(self):
        cleaned_data = super().clean()
        #self.cleaned_data['animalid'] = self.animalid 不要把无关的信息放这个类里了
        self.cleaned_data['method'] = 'virus inject'
        self.cleaned_data['parameters'] = {
            'virus_id': self.aavlist[int(cleaned_data.get('aav'))][1],
            'inject_method':self.inject_method_list[int(cleaned_data.get('inject_method'))][1],
            'inject_volumn':str(cleaned_data.get('inject_volumn')) +'ul',
            'inject_dose': cleaned_data.get('inject_dose'),
            'depth_num_of_each_spot': cleaned_data.get('depth_num_of_each_spot'),
            'inject_tool': self.inject_tool_list[int(cleaned_data.get('inject_tool'))][1]
        }

    # def save(self, commit=True): # 不管用不用这个，都只输入一个空的obj
    #     return super(AavinjectForm, self).save(commit=False)
    
class Setupwindow(forms.ModelForm):

    window_type = forms.ChoiceField(choices = [('glass','glass'), ('thin bone','thin bone')], initial = 'glass')
    layers = forms.ChoiceField(choices = [('5-3-3-3','5-3-3-3'), ('5-3-3','5-3-3')])
    with_agar = forms.ChoiceField(choices = [('Y','Y'), ('N','N')],initial = 'N')
    remove_dura = forms.ChoiceField(choices = [('Y','Y'), ('N','N')],initial = 'N')

    ap = forms.FloatField(label = 'AP (mm negative means rostral):')
    ml = forms.FloatField(label = 'ML (mm):')
    ref = forms.ChoiceField(label = 'reference: ', choices = [('lambda', 'lambda'), ('bregma', 'bregma')], initial = 'lambda')
    
    class Meta:
        model = SurgTreatment
        fields = ('date','time','note','window_type','layers',
            'with_agar','remove_dura'
        )
        widgets = {
            'date': forms.SelectDateWidget,
            'time': forms.DateInput(attrs={'class':'timepicker'})
        }

    def clean(self):
        cleaned_data = super().clean()
        self.cleaned_data['method'] = 'window setup'
        if cleaned_data.get('window_type') == 'glass':
            self.cleaned_data['parameters'] = {
                'window_type': cleaned_data.get('window_type'),
                'layers':cleaned_data.get('layers'),
                'with_agar':cleaned_data.get('with_agar'),
                'remove_dura':cleaned_data.get('remove_dura'),
                'location': 'reference: '+cleaned_data.get('ref')+'mm, AP '+str(cleaned_data.get('ap'))+'mm, ML '+str(cleaned_data.get('ml'))
            }
        elif cleaned_data.get('window_type') == 'thin bone':
            self.cleaned_data['parameters'] = {
                'window_type': cleaned_data.get('window_type')
            }

class Lfp(forms.ModelForm):
    wiretypelist = [
        ('0','tungsten, Bare = 0.002 in, Coated = 0.004 in, Pruduct = A-M Systems 795500'),
        ('1','silver, Bare = 0.005 in, Coated = NA, Pruduct = A-M Systems 781500')
    ]
    wire_type = forms.ChoiceField(
        choices = wiretypelist, 
        initial = '0'
    )
    ap = forms.FloatField(label = 'AP (mm negative means rostral):')
    ml = forms.FloatField(label = 'ML (mm):')
    ref = forms.ChoiceField(label = 'reference: ', choices = [('lambda', 'lambda'), ('bregma', 'bregma')], initial = 'lambda')
    
    class Meta:
        model = SurgTreatment
        fields = ('date','time','note','wire_type','ap','ml','ref')
        widgets = {
            'date': forms.SelectDateWidget,
            'time': forms.DateInput(attrs={'class':'timepicker'})
        }
    
    def clean(self):
        cleaned_data = super().clean()
        self.cleaned_data['method'] = 'lfp'
        self.cleaned_data['parameters'] = {
            'wire_type': self.wiretypelist[int(cleaned_data.get('wire_type'))][1],
            'location': 'reference: '+cleaned_data.get('ref')+'mm, AP '+str(cleaned_data.get('ap'))+'mm, ML '+str(cleaned_data.get('ml'))
        }

class Perfusion(forms.ModelForm):
    class Meta:
        model = SurgTreatment
        fields = ('date', 'time','note')
        widgets = {
            'date': forms.SelectDateWidget,
            'time': forms.DateInput(attrs={'class':'timepicker'})
        }
    def clean(self):
        cleaned_data = super().clean()
        self.cleaned_data['method'] = 'PFA purfusion'
        self.cleaned_data['parameters'] = {}