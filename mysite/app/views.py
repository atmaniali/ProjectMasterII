# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from django.views import generic
from django.views.generic import ListView
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.forms.widgets import DateTimeBaseInput
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from .form import *
from .models import *
from .utils import *
from ahpy import ahpy
from django.utils.dateparse import parse_datetime
import requests
import itertools
import csv
import numpy as np

@login_required(login_url="/login/")
def index(request):
    all_genders = requests.get('https://api.corona-dz.live/country/gender/all').json()
    all_country = requests.get('https://api.corona-dz.live/country/all').json()
    data = requests.get('https://api.corona-dz.live/country/latest').json()
    latest_age = requests.get('https://api.corona-dz.live/country/age/latest').json()
    date_auj = parse_datetime(data['date']).date()
    males = []
    females = []
    confirmedes = []
    dates_all_genderes = []
    for gnder in all_genders :
        males.append(gnder['male'])
        females.append(gnder['female'])
        dates_all_genderes.append(str(parse_datetime(gnder['date']).date()))
    for countrie in all_country:
        confirmedes.append(countrie['confirmed'])    
    context = {
        'response' : data,
        'date_de_donner' : date_auj
    } 
    if request.method == 'POST':
        id = request.POST.get('wilaya')
        urls = "https://api.corona-dz.live/province/{}/latest".format(id)
        wilaya_data = requests.get(urls).json()
        result = wilaya_data[0]
        final_result = result['data']
        context['wilaya'] = final_result[0]
    context['males'] = males[-6:]
    context['females'] = females [-6:] 
    context['date_all'] = dates_all_genderes [-6:] 
    context['latest_age'] = latest_age
    context['confirmedes'] = confirmedes[-6:]
    context['segment'] = 'index'
    html_template = loader.get_template( 'index.html' )
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        
        load_template      = request.path.split('/')[-1]
        context['segment'] = load_template
        
        html_template = loader.get_template( load_template )
        return HttpResponse(html_template.render(context, request))
        
    except template.TemplateDoesNotExist:

        html_template = loader.get_template( 'page-404.html' )
        return HttpResponse(html_template.render(context, request))

    except:
    
        html_template = loader.get_template( 'page-500.html' )
        return HttpResponse(html_template.render(context, request))


    # Home
def home_view(request):
    if request.is_ajax():
        res = request.POST.get('te') 
        res_int = int(res)
        print("type,",type(res_int))
        print("play",res_int)   
    context = {
        'response' : 'arwah netlag 3lik',     
    }
    context['segment'] = 'home'

    html_template = loader.get_template( 'home.html' )
    return HttpResponse(html_template.render(context, request)) 


def create(request):
    
    
        form = ContactForm(request.POST or None, instance= request.user.profile)
        if form.is_valid():
            form.save()
        pass
@login_required(login_url="/login/")
def profile(request):
    context = {}
    form = ContactForm(instance= request.user.profile)
    if request.method =='POST':
        form = ContactForm(request.POST or None, instance= request.user.profile)
        if form.is_valid():
            form.save()
            return redirect("app:profile")
        else:
            print("request not pass ")    
    context['form'] = form
    context['segment'] = 'profile'

    html_template = loader.get_template( 'profile.html' )
    return HttpResponse(html_template.render(context, request))      
    

#  hada test 
def create_critere_model_form(request):
    
    html_template = loader.get_template( 'haka.html' )
    context = {
    
    }
    return HttpResponse(html_template.render(context, request))     

# kayn jdid 3labali
# je c c c c         
def create_critere_normal(request):
    template_name = 'haka.html'
    heading_message = 'Formset Demo'    
    context = {}
    if request.method == 'GET':
        print("request.method == 'GET'", request.GET)
        formset = CritereFormset(request.GET or None)
    elif request.method == 'POST':
        formset = CritereFormset(request.POST)
        if formset.is_valid():
            csv_file = request.POST.get('input_name')
            for form in formset:
                name = form.cleaned_data.get('name')
                # save Critere instance
                if name:
                    
                    Critere(name=name).save()
                    # hada chkla 
            if len(csv_file ) != 0 :
                query = Critere.objects.all()
                # query_list = Critere.objects.all().count()
                list_critere = []
                for i in query:
                    list_critere.append(i.name) 
                list_np = np.array(list_critere) 
                matrix = [ [ 0 for i in range(len(list_np)) ] for j in range(len(list_np)) ]
                for i in range(len(list_np)):
                    for j in range(len(list_np)):
                        if i == j:
                            matrix[i][j] = 1
                    matrix_np = np.array(matrix) 
                    matrix_with_critere_ligne= np.vstack((list_np,matrix_np))
                    matrix_transpose = matrix_with_critere_ligne.transpose()
                    list_np_1 = np.append("",list_np)
                    matrix_with_critere_ligne_transpose= np.vstack((list_np_1,matrix_transpose))
                    pd.DataFrame(matrix_with_critere_ligne_transpose).to_csv("media/files/{}.csv".format(csv_file))        
            return redirect('app:critere_list')
    context['formset']=formset
    context['heading']=heading_message
    return render(request, template_name, context) 
    
class CritereListView(generic.ListView):

    model = Critere
    context_object_name = 'criteres'
    template_name = 'tables.html' 
    paginate_by = 5  
    ordering = ['-created_at']
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['subcritere_list'] = Subcritere.objects.all()
        return context
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            if request.POST.get('te') :
                id  = int(request.POST.get('te')) 
                objet = get_object_or_404(Critere, id = id)
                # objet.delete()
                print(id)
            if request.POST.get('tet'): 
                print("hi",request.POST.get('tet'))  
            if request.POST.get('test'): 
               print('oki')     
                  
        return render(request, self.template_name)    

def create_critere_with_subcritere(request):
    template_name = 'create_with_subcritere.html'
    if request.method == 'GET':
        print("get \t \n",request.GET)
        critereform = CritereModelForm(request.GET or None)
        formset = SubcritereFormset(queryset=Subcritere.objects.none())
    elif request.method == 'POST':
        print("post \t \n",request.POST)
        critereform = CritereModelForm(request.POST)
        print("critereform ", critereform )
        formset = SubcritereFormset(request.POST)
        print("formset", formset)
        if critereform.is_valid() and formset.is_valid():
            print("*********************************************")
            # first save this book, as its reference will be used in `Author`
            critere = critereform.save()
            for form in formset:
                # so that `book` instance can be attached.
                subcritere = form.save(commit=False)
                subcritere.critere = critere
                subcritere.save()
            return redirect('app:critere_list')
    return render(request, template_name, {
        'bookform': critereform,
        'formset': formset,
    }) 


import numpy as np
import pandas as pd
# TODO: delete   view
def save_critere_as_csv(request):
    print('a')
    """ A view that streams a large CSV file."""
    context = {} 
    
    query = Critere.objects.all()
    # query_list = Critere.objects.all().count()
    list_critere = []
    for i in query:
        list_critere.append(i.name) 
    list_np = np.array(list_critere) 
    matrix = [ [ 0 for i in range(len(list_np)) ] for j in range(len(list_np)) ]
    for i in range(len(list_np)):
        for j in range(len(list_np)):
            if i == j:
                matrix[i][j] = 1
    matrix_np = np.array(matrix) 
    matrix_with_critere_ligne= np.vstack((list_np,matrix_np))
    matrix_transpose = matrix_with_critere_ligne.transpose()
    list_np = np.append("",list_np)
    matrix_with_critere_ligne_transpose= np.vstack((list_np,matrix_transpose))    
    if request.method == 'POST':
        print(request.POST)
        print("request", request.POST)
        name = request.POST.get('input_name')
        print("name", name)
        data = pd.DataFrame(matrix_with_critere_ligne_transpose).to_csv("mysite/media/files/{}.csv".format(name)) 
        print("c bon", data) 
        return redirect("app:create_critere_normal")

    # context['segment'] = '#'
    html_template = loader.get_template( 'app:critere_list' )
    return HttpResponse(html_template.render(context, request)) 


import csv 
def convert_to_tuple(list):
    return tuple(list)   
def show_resultat(request):
    html_template = loader.get_template( 'result_critere.html' )
    context = {}
    dictionnaire = {}
    Matrix = np.array(list(csv.reader(open("media/files/data2.csv", "r"), delimiter=",")))
    matrix_list = Matrix[2:,1]
    matrix = Matrix[2:,2:].astype(float)
    for i in range(len(matrix_list)):
        for j in range(len(matrix_list)):
            if i < j:
                dictionnaire.update({(matrix_list[i],matrix_list[j]):matrix[i][j]})
    donner = Save_result(name = "critere_generale", dictionnaire = dictionnaire)
    donner.save()
    print("data is upload", donner)
    critere  = Critere.objects.all()
    # sub = critere.subcritere_set.all()   
    if request.method == 'POST':
        pk_critere = request.POST.get("critere_drop_text")   
        cr = Critere.objects.get(pk= pk_critere) 
        # sub = cr.subcriters.all()
        list_sub = [e.name for e in cr.subcriters.all()]
        print("sub_critere", cr.subcriters.all())
        print([e.name for e in cr.subcriters.all()])
        # start script.py to prepar csv fille for  subcritere :
        list_np = np.array(list_sub)
        matrix = [ [ 0 for i in range(len(list_sub)) ] for j in range(len(list_sub)) ]
        for i in range(len(list_sub)):
            for j in range(len(list_sub)):
                if i == j:
                    matrix[i][j] = 1
        matrix_np = np.array(matrix) 
        matrix_with_critere_ligne= np.vstack((list_np,matrix_np))
        print("matrix_critere ligne \n",matrix_with_critere_ligne)
        matrix_transpose = matrix_with_critere_ligne.transpose()
        print(matrix_transpose)
        list_np_1 = np.append("",list_np)
        print(list_np_1)
        matrix_with_critere_ligne_transpose= np.vstack((list_np_1,matrix_transpose))
        print(matrix_with_critere_ligne_transpose)
        pd.DataFrame(matrix_with_critere_ligne_transpose).to_csv("media/files/data2_subcritere.csv")
        
    context["dictionnaire"] = dictionnaire 
    context["critere"] = critere  
    # context["sub"] = list_sub
    return HttpResponse(html_template.render(context, request))   

def save_as_csv(query, name):
    list_np = np.array(query) 
    matrix = [ [ 0 for i in range(len(query)) ] for j in range(len(query)) ]
    for i in range(len(query)):
        for j in range(len(query)):
            if i == j:
                matrix[i][j] = 1
    matrix_np = np.array(matrix)  
    matrix_with_critere_ligne= np.vstack((list_np,matrix_np))
    matrix_transpose = matrix_with_critere_ligne.transpose()
    list_np = np.append("",list_np)
    matrix_with_critere_ligne_transpose= np.vstack((list_np,matrix_transpose))
    pd.DataFrame(matrix_with_critere_ligne_transpose).to_csv("media/files/critere_{}.csv".format(name))

def from_csv_to_dict(file):
    dictionnaire = {}
    Matrix = np.loadtxt(file,dtype = str, skiprows=0, delimiter=',')
    matrix_list = Matrix[0,1:]
    matrix = Matrix[1:,1:].astype(float)
    for i in range(len(matrix_list)):
        for j in range(len(matrix_list)):
            if i < j:
                dictionnaire.update({(matrix_list[i],matrix_list[j]):matrix[i][j]})             
    return dictionnaire 
def from_csv_to_tuple(file, type):
    Matrix = np.loadtxt(file,dtype = type, skiprows=0, delimiter=',')
    tuples = tuple(Matrix)
    return tuples    

def tester_chkla_ta3i(request):
    """ in this function  i want to show result from models and csv file """
    # 
    # first we need to load csv file & turn it to dictionnaire
    dict = {}
    context= {}
    critere = Critere.objects.all()
    list_critere = []
    for i in critere:
        list_critere.append(i.name) 
    print(critere,"\n",list_critere)    
    save_as_csv(list_critere,"cri")
    file = "media/files/data2.csv"
    dict = from_csv_to_dict(file)
    print(dict)
        
    html_template = loader.get_template( 'tester_chkla_ta3i.html' )
    return HttpResponse(html_template.render(context, request)) 

# HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH          
def promether_view(request) :
    context = {}
    if request.method == 'POST':
        doc_file=request.FILES.get('myfile')
        weight_file = request.FILES.get('myfile1')
        mat = np.loadtxt(doc_file,dtype = str, skiprows=0, delimiter=',')
        print("matric",mat)        
        context['mat'] = mat  
        result = readMatrix(doc_file, weight_file) 
        context['result'] = result  
    html_template = loader.get_template( 'promethee_2_page.html' )
    return HttpResponse(html_template.render(context, request))
import itertools
def ahp_final(request):
    html_template = loader.get_template( 'ahp_final.html')
    context = {}
    if request.method == 'POST':
        # upoad csv file
        # dictionnaire
        critere_file = request.FILES.get('critere')
        caracteristique_vaccin_file = request.FILES.get('caracteristique_vaccin')
        posologie_file = request.FILES.get('posologie')
        cout_file = request.FILES.get('cout')
        effets_secondaire_file = request.FILES.get('effets_secondaire')
        # tuple
        alternatives_file = request.FILES.get('alternatives')
        type_file = request.FILES.get('type')
        efficacite_file = request.FILES.get('efficacite')
        nbr_dose_file = request.FILES.get('nbr_dose')
        age_file = request.FILES.get('age')
        delais_file = request.FILES.get('delais')
        temps_effet_file = request.FILES.get('temps_effet')
        conservation_file = request.FILES.get('conservation')
        prix_file = request.FILES.get('prix')
        sen_au_point_file = request.FILES.get('sen_au_point')
        doul_au_point_file = request.FILES.get('doul_au_point')
        cephales_file = request.FILES.get('cephales')
        hyperthermie_file = request.FILES.get('hyperthermie')
        nausees_file = request.FILES.get('nausees')
        fatigue_file = request.FILES.get('fatigue')
        # csv_to_dictionaire
        critere_filecsv = from_csv_to_dict(critere_file)
        caracteristique_vaccin_filecsv = from_csv_to_dict(caracteristique_vaccin_file)
        posologie_filecsv = from_csv_to_dict(posologie_file)
        cout_filecsv = from_csv_to_dict(cout_file)
        effets_secondaire_filecsv = from_csv_to_dict(effets_secondaire_file)
        # csv_to_tuple
        alternatives_filecsv = from_csv_to_tuple(alternatives_file,str)
        type_filecsv = from_csv_to_tuple(type_file,float)
        efficacite_filecsv = from_csv_to_tuple(efficacite_file,float)
        nbr_dose_filecsv = from_csv_to_tuple(nbr_dose_file,float)
        age_filecsv = from_csv_to_tuple(age_file,float)
        delais_filecsv = from_csv_to_tuple(delais_file,float)
        temps_effet_filecsv  = from_csv_to_tuple(temps_effet_file,float)
        conservation_filecsv = from_csv_to_tuple(conservation_file,float)
        prix_filecsv = from_csv_to_tuple(prix_file,float)
        sen_au_point_filecsv = from_csv_to_tuple(sen_au_point_file,float)
        doul_au_point_filecsv = from_csv_to_tuple(doul_au_point_file,float)
        cephales_filecsv = from_csv_to_tuple(cephales_file,float)
        hyperthermie_filecsv = from_csv_to_tuple(hyperthermie_file,float)
        nausees_filecsv = from_csv_to_tuple(nausees_file,float)
        fatigue_filecsv = from_csv_to_tuple(fatigue_file,float)
        # start methode 
        critere_comparison = critere_filecsv
        criteria = ahpy.Compare('Criteria', critere_comparison, precision=3)
        print("criteria \n",criteria.target_weights)
        caracterisiqueVaccin_comparison = caracteristique_vaccin_filecsv
        posologie_comparisons = posologie_filecsv
        cout_comparisons = cout_filecsv
        effets_secondaire_comparisons = effets_secondaire_filecsv
        vaccins = alternatives_filecsv
        vaccin_pairs = list(itertools.combinations(vaccins, 2))
        type_values = type_filecsv
        type_comparisons = dict(zip(vaccin_pairs, type_values))
        effecacite_values = efficacite_filecsv
        effecacite_comparisons = dict(zip(vaccin_pairs, effecacite_values))
        nbr_dose_values = nbr_dose_filecsv
        nbr_dose_comparisons = dict(zip(vaccin_pairs, nbr_dose_values))
        age_values = age_filecsv 
        age_comparisons = dict(zip(vaccin_pairs, age_values))
        delais_values = delais_filecsv
        delais_comparisons = dict(zip(vaccin_pairs, delais_values))
        temps_effet_values = temps_effet_filecsv
        temps_effet_comparisons = dict(zip(vaccin_pairs, temps_effet_values))
        conservation_values = conservation_filecsv
        conservation_comparisons = dict(zip(vaccin_pairs, conservation_values))
        prix_values = prix_filecsv 
        prix_comparisons = dict(zip(vaccin_pairs, prix_values))
        sapi_values = sen_au_point_filecsv
        sapi_comparisons = dict(zip(vaccin_pairs, sapi_values))
        dapi_values = doul_au_point_filecsv 
        dapi_comparisons = dict(zip(vaccin_pairs, dapi_values))
        print("dapi_comparisons \n",dapi_comparisons)
        cephalees_values = cephales_filecsv
        cephalees_comparisons = dict(zip(vaccin_pairs, cephalees_values))
        hyperthermie_values = hyperthermie_filecsv
        hyperthermie_comparisons = dict(zip(vaccin_pairs, hyperthermie_values))
        nausées_values = nausees_filecsv
        nausées_comparisons = dict(zip(vaccin_pairs, nausées_values))
        fatigue_values = fatigue_filecsv 
        fatigue_comparisons = dict(zip(vaccin_pairs, fatigue_values))
        caracteristique_vacc = ahpy.Compare('CarachterisiqueVaccin', caracterisiqueVaccin_comparison, precision=3)
        posologie = ahpy.Compare('Posologie', posologie_comparisons, precision=3)
        print("posologie \n",posologie.target_weights)
        cout = ahpy.Compare('Cout', cout_comparisons, precision=3)
        effait_sec = ahpy.Compare('EffetsSecondaire', effets_secondaire_comparisons, precision=3)
        type_s = ahpy.Compare('Type', type_comparisons, precision=3)
        efficacite = ahpy.Compare('Efficacite', effecacite_comparisons, precision=3)
        nbr_dose = ahpy.Compare('NBrDose', nbr_dose_comparisons, precision=3)
        age = ahpy.Compare('Age', age_comparisons, precision=3)
        delais = ahpy.Compare('Delais', delais_comparisons, precision=3)
        temp_eff = ahpy.Compare('Temps_d_effet', temps_effet_comparisons, precision=3)
        conservation = ahpy.Compare('Conservation', conservation_comparisons, precision=3)
        prix = ahpy.Compare('Prix', prix_comparisons, precision=3)
        sapi = ahpy.Compare('sensibilité_au_point_injection', sapi_comparisons, precision=3)
        dapi = ahpy.Compare('douleur_au_point_injection', dapi_comparisons, precision=3)
        cephalees = ahpy.Compare('céphalées', cephalees_comparisons, precision=3)
        hyperthermie = ahpy.Compare('hyperthermie', hyperthermie_comparisons, precision=3)
        nausees = ahpy.Compare('nausées', nausées_comparisons, precision=3)
        fatigue = ahpy.Compare('fatigue', fatigue_comparisons, precision=3)
        print("fatigue \n", fatigue.target_weights)
        print("fatigue type \n", type(fatigue.target_weights))
       # link all comparte object in hearchy
        caracteristique_vacc.add_children([type_s,efficacite])
        posologie.add_children([nbr_dose,age,delais,temp_eff])
        cout.add_children([conservation,prix])
        effait_sec.add_children([sapi,dapi,cephalees,hyperthermie,nausees,fatigue])
        criteria.add_children([caracteristique_vacc,posologie,cout,effait_sec])
        print("cr", criteria)
        print("final criteria \n", criteria.target_weights)
        keys = []
        values = []
        # TODO: result doesn't work
        result = criteria.target_weights
        # print(criteria.target_weights)
        for key, val in result.items():
            keys.append(key)
            values.append(val)
        context['final'] = criteria.target_weights
        context['keys'] = keys
        context['values'] = values
    return HttpResponse(html_template.render(context, request))    





   
    
    


