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
from ahpy import ahpy
from django.utils.dateparse import parse_datetime
import requests
import itertools
import csv
import numpy as np

@login_required(login_url="/login/")
def index(request):
    all_genders = requests.get('https://api.corona-dz.live/country/gender/all').json()
    data = requests.get('https://api.corona-dz.live/country/latest').json()
    date_auj = parse_datetime(data['date']).date()
    males = []
    females = []
    dates_all_genderes = []
    for gnder in all_genders :
        males.append(gnder['male'])
        females.append(gnder['female'])
        dates_all_genderes.append(str(parse_datetime(gnder['date']).date()))
    context = {
        'response' : data,
        'date_de_donner' : date_auj
    }  
    context['males'] = males[-6:]
    context['females'] = females [-6:] 
    context['date_all'] = dates_all_genderes [-6:] 
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
# TODO: delete   view
def api(request):
    data = requests.get('https://api.corona-dz.live/country/latest').json()
    print('Hello ')
    context = {
        'response' : 'arwah netlag 3lik',
         'data' : data
    }
    context['segment'] = 'api'

    html_template = loader.get_template( 'api.html' )
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
# TODO: delete   view
def api2(request):
    dates = []
    data = requests.get('https://api.corona-dz.live/country/all').json()
    print('Hello 2')
    deathes = []
    for i in data:
        print("type dates", type(parse_datetime(i['date'])))
        dates.append(parse_datetime(i['date']).date())
        deathes.append(i['deaths'])
    context = {
        'response' : 'arwah netlag 3lik',
        'data' : data,
        'dates' : dates,
        'deathes': deathes
    }
    context['segment'] = 'api2'

    html_template = loader.get_template( 'api2.html' )
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
# TODO: delete   view
# Vaccins
def vccins_page(request):
    context = {} 
    # if request.method =='POST':
    #     vaccin_form = VaccinsForm(request.POST or None)
    #     effets_secondaire_form = Effets_secondairesForm(request.POST or None)
    #     cout_form = CoutForm(request.POST or None)
    #     posologie_form = PosologieForm(request.POST or None)
    #     charachteristique_form= CharacteristiquesForm(request.POST or None)
    #     if vaccin_form.is_valid():
    #         vaccin_nom = vaccin_form.cleaned_data['nom_vaccin']
    #         if effets_secondaire_form.is_valid():
    #             obj1 = effets_secondaire_form.save()
    #             # 
    #         if cout_form.is_valid():
    #             obj2 = cout_form.save()
    #                 #
    #         if posologie_form.is_valid():
    #             obj3 = posologie_form.save()

    #         if charachteristique_form.is_valid():
    #             obj4 = charachteristique_form.save()
                
    #         vaccin = Vaccins.objects.create(nom_vaccin = vaccin_nom, effets_secondaires = obj1,
    #         Characteristiques =  obj4,
    #         posologie = obj3,
    #         cout = obj2)    
    #         vaccin.save()
    #         return redirect('vaccins.html')    
    # else:
    #     vaccin_form = VaccinsForm()
    #     effets_secondaire_form = Effets_secondairesForm()
    #     cout_form = CoutForm()
    #     posologie_form = PosologieForm()
    #     charachteristique_form= CharacteristiquesForm()
              
    # context['effets_secondaire_form'] = effets_secondaire_form
    # context['cout_form'] = cout_form
    # context['posologie_form'] = posologie_form
    # context['charachteristique_form'] = charachteristique_form
    # context['vaccin_form'] = vaccin_form
    context['segment'] = 'profile'

    html_template = loader.get_template( 'vaccins.html' )
    return HttpResponse(html_template.render(context, request))    
# TODO: delete   view
def data_page(request):
    
    males = []
    females = []
    context= {}
    context['segment'] = 'data_page'
    drink_comparisons = {('coffee', 'wine'): 9, ('coffee', 'tea'): 5, ('coffee', 'beer'): 2, ('coffee', 'soda'): 1,
                          ('coffee', 'milk'): 1, ('coffee', 'water'): 1 / 2,
                          ('wine', 'tea'): 1 / 3, ('wine', 'beer'): 1 / 9, ('wine', 'soda'): 1 / 9,
                          ('wine', 'milk'): 1 / 9, ('wine', 'water'): 1 / 9,
                          ('tea', 'beer'): 1 / 3, ('tea', 'soda'): 1 / 4, ('tea', 'milk'): 1 / 3,
                          ('tea', 'water'): 1 / 9,
                          ('beer', 'soda'): 1 / 2, ('beer', 'milk'): 1, ('beer', 'water'): 1 / 3,
                          ('soda', 'milk'): 2, ('soda', 'water'): 1 / 2,
                          ('milk', 'water'): 1 / 3}
    drinks = ahpy.Compare(name='Drinks', comparisons=drink_comparisons, precision=3, random_index='saaty') 
    dicti = drinks.target_weights
    dict_items = dicti.items()
    context['drink_comparaison'] = drink_comparisons
    context['target_weights'] = drinks.target_weights
    context['dictonary_items'] = dict_items
    
    html_template = loader.get_template( 'donner.html' )
    return HttpResponse(html_template.render(context, request)) 
# TODO: delete   view    
    # AHP methode 
def ahp_page(request):
    print('salam')
    genders = requests.get('https://api.corona-dz.live/country/gender/latest').json()
    all_genders = requests.get('https://api.corona-dz.live/country/gender/all').json()
    sexe = ['male', 'female']
    males = []
    females = []
    dates_all_genderes = []
    sexe_values = []
    sexe_values.append(genders['male'])
    sexe_values.append(genders['female'])
# remplire  all gender male female with  dates
    for gnder in all_genders :
        males.append(gnder['male'])
        females.append(gnder['female'])
        # recupirer date sous forme 'dd/mm/yyyy' et turn in string
        dates_all_genderes.append(str(parse_datetime(gnder['date']).date()))
        
    context = {}
    print('male .', males[:5])
    print('dates ***************** .', dates_all_genderes[-5:])
    x = dates_all_genderes[1]
    print('type dates !:', type(str(x)))

    # URL  example : https://en.wikipedia.org/wiki/Analytic_hierarchy_process_–_car_example  
    # Creteria
    criteria_comparisons = {('Cost', 'Safety'): 3, ('Cost', 'Style'): 7, ('Cost', 'Capacity'): 3,
    ('Safety', 'Style'): 9, ('Safety', 'Capacity'): 1,
    ('Style', 'Capacity'): 1/7}
    criteria = ahpy.Compare('Criteria', criteria_comparisons, precision=3)
    # Show all of criteria report
    report_creteria = criteria.report(show=True)
    # 
    print("type of report creteria",type(report_creteria))
    # Subcreteria :
    # Coast comparison have 4 subcreteria  
    cost_comparisons = {('Price', 'Fuel'): 2, ('Price', 'Maintenance'): 5, ('Price', 'Resale'): 3,
    ('Fuel', 'Maintenance'): 2, ('Fuel', 'Resale'): 2,
    ('Maintenance', 'Resale'): 1/2}
    #  Capacitycreia have 2 subcreteria
    capacity_comparisons = {('Cargo', 'Passenger'): 1/5}
    # Alternative we have : 6
    vehicles = ('Accord Sedan', 'Accord Hybrid', 'Pilot', 'CR-V', 'Element', 'Odyssey')
    # make theme en 2 pairs
    vehicle_pairs = list(itertools.combinations(vehicles, 2))
    print(vehicle_pairs)
    # we made relation alternative subcreteria
    # {Start}
    price_values = (9, 9, 1, 1/2, 5, 1, 1/9, 1/9, 1/7, 1/9, 1/9, 1/7, 1/2, 5, 6)
    price_comparisons = dict(zip(vehicle_pairs, price_values))
    print(price_comparisons)
    safety_values = (1, 5, 7, 9, 1/3, 5, 7, 9, 1/3, 2, 9, 1/8, 2, 1/8, 1/9)
    safety_comparisons = dict(zip(vehicle_pairs, safety_values))

    passenger_values = (1, 1/2, 1, 3, 1/2, 1/2, 1, 3, 1/2, 2, 6, 1, 3, 1/2, 1/6)
    passenger_comparisons = dict(zip(vehicle_pairs, passenger_values))

    fuel_values = (1/1.13, 1.41, 1.15, 1.24, 1.19, 1.59, 1.3, 1.4, 1.35, 1/1.23, 1/1.14, 1/1.18, 1.08, 1.04, 1/1.04)
    fuel_comparisons = dict(zip(vehicle_pairs, fuel_values))

    resale_values = (3, 4, 1/2, 2, 2, 2, 1/5, 1, 1, 1/6, 1/2, 1/2, 4, 4, 1)
    resale_comparisons = dict(zip(vehicle_pairs, resale_values))

    maintenance_values = (1.5, 4, 4, 4, 5, 4, 4, 4, 5, 1, 1.2, 1, 1, 3, 2)
    maintenance_comparisons = dict(zip(vehicle_pairs, maintenance_values))

    style_values = (1, 7, 5, 9, 6, 7, 5, 9, 6, 1/6, 3, 1/3, 7, 5, 1/5)
    style_comparisons = dict(zip(vehicle_pairs, style_values))

    cargo_values = (1, 1/2, 1/2, 1/2, 1/3, 1/2, 1/2, 1/2, 1/3, 1, 1, 1/2, 1, 1/2, 1/2)
    cargo_comparisons = dict(zip(vehicle_pairs, cargo_values))
    # {End}
    # startcalcul
    # create corresponding Compare objects:
    cost = ahpy.Compare('Cost', cost_comparisons, precision=3)
    capacity = ahpy.Compare('Capacity', capacity_comparisons, precision=3)
    price = ahpy.Compare('Price', price_comparisons, precision=3)
    safety = ahpy.Compare('Safety', safety_comparisons, precision=3)
    passenger = ahpy.Compare('Passenger', passenger_comparisons, precision=3)
    fuel = ahpy.Compare('Fuel', fuel_comparisons, precision=3)
    resale = ahpy.Compare('Resale', resale_comparisons, precision=3)
    maintenance = ahpy.Compare('Maintenance', maintenance_comparisons, precision=3)
    style = ahpy.Compare('Style', style_comparisons, precision=3)
    cargo = ahpy.Compare('Cargo', cargo_comparisons, precision=3)
    # End calcul
    # The final step is to link all of the Compare objects into a hierarchy. First, 
    # we'll make the Price, Fuel, Maintenance and Resale objects the children of the Cost object...
    cost.add_children([price, fuel, maintenance, resale])
    capacity.add_children([cargo, passenger])
    # Now that the hierarchy represents the decision problem, 
    # we can print the target weights of the highest level Criteria object to see the results of the analysis:
    criteria.add_children([cost, safety, style, capacity])
    print(criteria.target_weights)
    dicti = criteria.target_weights
    dict_items = dicti.items()
    queryset_count = Resultat.objects.count()
    if queryset_count == 0:
        for keys, values in dict_items:
            result = Resultat(key = keys, value = values)
            result.save()
            print("type of key",type(keys), "values = ",keys)
            print("type of value",type(values), "values = ",values)
    # PROMETH II
    # Matrix = np.array(list(csv.reader(open("media/files/promethee_testing.csv", "r"), delimiter=",")))
    # print('Matrice de performance',Matrix)
    # array_Matrix  = np.array(Matrix)
    # Alternative_matix = array_Matrix[2:,1:].astype(np.single)
    # labels = array_Matrix[0,1:]
    # Alternatives = array_Matrix[2:,0]
    # maximisation = array_Matrix[1,1:]
    # min_criteria_array = Alternative_matix.min(axis=0)
    # max_criteria_array = Alternative_matix.max(axis=0)
    # for i in range(len(Alternative_matix)):
    #     for j in range(len(Alternative_matix[i])):
    #         if maximisation[j] == 'yes':
    #             Alternative_matix[i][j] = (max_criteria_array[j]-Alternative_matix[i][j])/(max_criteria_array[j]-min_criteria_array[j])
    #         else:
    #             Alternative_matix[i][j] = (Alternative_matix[i][j]-min_criteria_array[j])/(max_criteria_array[j]-min_criteria_array[j])


            
    context['dictonary_items'] = dict_items
    context['genders'] = genders
    context['sexe'] = sexe
    context['sexe_values'] = sexe_values
    # report = criteria.report(show=True)
    # report = cost.report(show=True)
    queryset  = Resultat.objects.all()
    labels = []
    data = []
    for result in queryset:
        labels.append(result.key)
        data.append(result.value)
    context['labels'] = labels
    context['data'] = data 
    context['males'] = males[:20]
    context['females'] = females [:20] 
    context['date_all'] = dates_all_genderes[:20]
    print(genders['male']) 
    html_template = loader.get_template( 'donner.html' )
    return HttpResponse(html_template.render(context, request))    
#  test_ahp/ pages   
def test_ahp_view(request):
    context = {}
    context['segment'] = 'test_ahp'
    html_template = loader.get_template( 'haka.html' )
    if request.method == 'GET':
        formset = CritereFormset(request.GET or None)
    elif request.method == 'POST':
        formset = CritereFormset(request.POST)
        if formset.is_valid():
            for form in formset:
                # extract name from each form and save
                name = form.cleaned_data.get('name')
                # save book instance
                if name:
                    Critere(nom_critere=name).save()
            # once all books are saved, redirect to book list view
            return redirect('haka.html')
    # return render(request, template_name, {
    #     'formset': formset,
    #     'heading': heading_message,
    # })
    context['formset'] = formset
    # context['segment'] = 'test_ahp'
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
# TODO: delete   view    
class  teser_tableau_ta3k(ListView):
    model = Critere
    context_object_name = 'criteres'
    template_name = 't3_tableau.html'
# TODO: delete   view
import csv  
import numpy as np
def test_csv_ahp(request) :
    template_name = 't3_tableau.html'
    query = Critere.objects.all()
    query_list = Critere.objects.all().count()
    list_critere = []
    for i in query:
        list_critere.append(i.name) 
    list_np = np.array(list_critere) 
    hak = np.array(["a","b","c","d","e","f"])   
    matrix = [ [ 1 for i in range(query_list) ] for j in range(query_list) ]
    matrix_np = np.array(matrix)  
    print("matrix_np  \n",matrix_np)
    print("matrix", matrix)
    matrix_with_critere_ligne = np.vstack((list_np,matrix_np))
    print("matrix_critere  \n",matrix_with_critere_ligne)
    matrix_with_critere_clmn = np.hstack((hak, matrix_with_critere_ligne))
    print("matrix_critere  \n",matrix_with_critere_clmn)
    context = {}
    return render(request, template_name, context)  

# this view for save critere as csv fiele
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
def aimen_methode(request):
    html_template = loader.get_template( 'aimen.html' )
    context = {}
    criteres_values = []
    query = Critere.objects.all()
    # query_list = Critere.objects.all().count()
    list_critere = []
    dictionnaire = {}
    for i in query:
        list_critere.append(i.name) 
    list_np = np.array(list_critere) 
    print("hdi ydra",list_np)
    if request.method == 'GET':
        # name = request.POST.get('input_name')
        for i in range(len(list_np)):
            for j in range(len(list_np)):
                if i < j:
                    dictionnaire.update({(list_critere[i],list_critere[j]):float(request.POST.get('{}-{}'.format(list_critere[i], list_critere[j])))})
        print("hada howa ****", dictionnaire)
    context["criteres"] = list_np
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
    Matrix = np.array(list(csv.reader(open(file, "r"), delimiter=",")))
    matrix_list = Matrix[2:,1]
    matrix = Matrix[2:,2:].astype(float)
    for i in range(len(matrix_list)):
        for j in range(len(matrix_list)):
            if i < j:
                dictionnaire.update({(matrix_list[i],matrix_list[j]):matrix[i][j]})    
    return dictionnaire 

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

def chart_for(request):
    context= {}
    all_genders = requests.get('https://api.corona-dz.live/country/gender/all').json()
    males = []
    females = []
    dates_all_genderes = []
    for gnder in all_genders :
        males.append(gnder['male'])
        females.append(gnder['female'])
        dates_all_genderes.append(str(parse_datetime(gnder['date']).date()))
    context['males'] = males[-6:]
    context['females'] = females [-6:] 
    context['date_all'] = dates_all_genderes [-6:] 
    html_template = loader.get_template( 'chart4.html' )
    return HttpResponse(html_template.render(context, request))
# promethee II : 
from django.conf import settings
import numpy
from django.core.files.storage import FileSystemStorage

def all_alternatives(Alternatives):
    Alternative_possibilities = []
    for i in range(len(Alternatives)):
        for j in range(len(Alternatives)):
            if i == j:
                pass
            else:
                Alternative_possibilities.append(Alternatives[i]+'-'+Alternatives[j])
    return np.array(Alternative_possibilities).reshape(len(Alternative_possibilities),1)
# create the matrix of all variables possibilities:
def all_variables(matrix):
    new_matrix = []
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if i == j:
                pass
            else:
                new_matrix.append(matrix[i]-matrix[j])
    return np.array(new_matrix)    
def changetozeros(matrix):
    for i in range(len(matrix)) :  
        for j in range(len(matrix[i])) :  
            if matrix[i][j] < 0 :
                matrix[i][j] = 0
    return matrix  
def mult_matrix_vect(matrix, weight):
    for i in range(len(matrix)) :  
        for j in range(len(matrix[i])) :  
            matrix[i][j] = matrix[i][j]* weight[j]
    return matrix
def show_mult_matrix_vect(matrix, weight):
    data = []
    for i in range(len(matrix)) :  
       
        for j in range(len(matrix[i])) : 
           
            data.append('{}*{}'.format(weight[j],matrix[i][j]))
    return np.array(data)   
def add_aggregated_preferences_line(matrix):
    average_line_weight = []
    
    for i in range(len(matrix)) :
        sum = 0  
        for j in range(len(matrix[i])) :
            sum = sum + matrix[i][j] 
        average_line_weight.append(sum)
        
    matrix = np.vstack([matrix.transpose(), average_line_weight]).transpose()
    return matrix  
def create_aggregated_matrix(matrix, aggr):
    # retrieve only the aggregated column(list)
    aggregate_column = np.array(matrix[:, -1].transpose())
    agrs = aggr.tolist()
    print(aggregate_column)
    print("type of aggregate_column")
    print(type(aggregate_column))
    aggregated_matrix = [ [ 0 for i in range(len(matrix)) ] for j in range(len(matrix)) ]
    for i in range(len(matrix)) :  
        print("***//****aggregated matrix*//**", len(aggregated_matrix))
        print("***//**len matrix**//**", len(matrix))
        for j in range(len(matrix[i])) :       
            if i == j:
                aggregated_matrix[i][j] = 0        
            else:  
                aggregated_matrix[i][j]= agrs[0]
                agrs.pop(0) 
            
                
                # aggregated_matrix.append(aggregate_column[j])
    # print('lol',aggregated_matrix)
    print(np.array(aggregated_matrix).shape)
    return aggregated_matrix
           
def sumColumn(matrice):
    return [sum(col) for col in zip(*matrice)] 
def calculateflows(matrix):
    diffs=[]
    for i in range(len(matrix)):
        diffs.append(matrix[i,-1] - matrix[-1, i])
    return diffs

# HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH          
def promether_view(request) :
    context = {}
    # if request.method == 'POST' and request.FILES['excel_file']:
    #     print("did")
    #     fileb = request.FILES['excel_file']
    #     print(fileb)
        # fs = FileSystemStorage()
        # filename = fs.save(file.name, file)
        # uploaded_file_url = fs.url(filename) 
    print("promethee II")
    file = "/home/ali/Documents/MasterIIproect/mysite/app/file.csv"
    fil = "/home/ali/Documents/MasterIIproect/MP.csv"
    # Matrix = np.array(list(csv.reader(open(file, "r"), delimiter=",")))
    Matrix = np.loadtxt(fil,dtype = str, skiprows=0, delimiter=',')
    # STEP 1 : Normalize the Evaluation Matrix
    array_Matrix  = np.array(Matrix)
    Alternative_matix = array_Matrix[2:,1:].astype(np.single)
    print('Alternative_matix \n',Alternative_matix)
    labels = array_Matrix[0,1:]
    print('labels \n',labels)
    Alternatives = array_Matrix[2:,0]
    print('Names \n',Alternatives)
    maximisation = array_Matrix[1,1:]
    print('Beneficial or Not  \n',maximisation)
    # Get min and max for each criteria
    min_criteria_array = Alternative_matix.min(axis=0)
    print('min_criteria_array \n',min_criteria_array)
    max_criteria_array = Alternative_matix.max(axis=0)
    print('max_criteria_array \n',max_criteria_array)
    for i in range(len(Alternative_matix)):
        for j in range(len(Alternative_matix[i])):
            if maximisation[j] == 'yes':
                Alternative_matix[i][j] = (max_criteria_array[j]-Alternative_matix[i][j])/(max_criteria_array[j]-min_criteria_array[j])
            else:
                Alternative_matix[i][j] = (Alternative_matix[i][j]-min_criteria_array[j])/(max_criteria_array[j]-min_criteria_array[j])
    print('Alternative_matix \n',Alternative_matix)
    # STEP 2 : Calculate Evaluative ieme per the othere {m1-m2 | m1-m3 | ....}
    # Create the Alternatives Possibilities array[m1-m2,........]              
    Alternative_possibilities = all_alternatives(Alternatives)
    print('Alternative_possibilities \n', Alternative_possibilities)
    # create the matrix of all variables possibilities:
    variables_possibilities = all_variables(Alternative_matix)
    print('variables_possibilities \n', variables_possibilities)
    print('Alternative_possibilities shape \n', Alternative_possibilities.shape)
    print('variables_possibilities shape \n', variables_possibilities.shape)
    # concatenate the Names and variables related 
    the_all_matrix = np.hstack([Alternative_possibilities, variables_possibilities])
    print('The All Matrix \n', the_all_matrix)
    # "STEP 3 : Calculate the PREFERENCE Function"
    # Create an updated matrix that return 0 if value is negative or equal to 0 
    # else keep value as it it
    Preference_matrix = changetozeros(variables_possibilities)
    print('PREFERENCE_matrix \n', Preference_matrix)
    # time.sleep(3)
    # concatenate the Names and preferences related 
    the_Preference_matrix = np.hstack([Alternative_possibilities, Preference_matrix])
    print('the_Preference_matrix \n', the_Preference_matrix)
    weights =list(csv.reader(open("/home/ali/Documents/MasterIIproect/weight.csv", "r"), delimiter=","))  
    print('weights \n', weights)
    array_weights = np.asarray(weights[0], dtype='float')
    print('array_weights \n', array_weights)
    Agregate_preference_matrix = mult_matrix_vect(Preference_matrix, array_weights)
    show_calculation = show_mult_matrix_vect(Preference_matrix, array_weights)
    # lets add a column to sum these aggregated preferences
    Agregate_preference_matrix_with_sum = add_aggregated_preferences_line(Agregate_preference_matrix)
    print('Agregate_preference_matrix_with_sum \n', Agregate_preference_matrix_with_sum)
# time.sleep(3)
    aggrsums = Agregate_preference_matrix_with_sum[:,-1]
    print(aggrsums)

# take only the aggragated sum values(LAST column) and create aggregated preference Function(matrix)
    aggregated_matrix = np.zeros((len(Alternatives), len(Alternatives)))

    print("len alternatives")
    created_aggregated_matrix = create_aggregated_matrix(aggregated_matrix, aggrsums)

    print("HADA created_aggregated_matrix")
    print(created_aggregated_matrix)
    # time.sleep(3)
    duplicated = created_aggregated_matrix
    #flot entrant w sortant
    sommeeecolonne= sumColumn(created_aggregated_matrix)

    sumrows = np.sum(created_aggregated_matrix, axis = 1)
    #we need to deivde those calculated values on the number of alternatives -1
    newsommecolonne = []
    newsumrow= []
    for x in sommeeecolonne:
        newsommecolonne.append(x /(len(created_aggregated_matrix) - 1))

    for x in sumrows:
        newsumrow.append(x /(len(created_aggregated_matrix) - 1))
    
    print("flots entrants \n" , newsommecolonne)
    print("flots sortants \n" , newsumrow)

    created_aggregated_matrix = np.vstack([created_aggregated_matrix, newsumrow])
    print("updated matrix with columns ")
    print(created_aggregated_matrix)

    newsommecolonne.append(0)
    created_aggregated_matrix= np.vstack([created_aggregated_matrix.transpose(), newsommecolonne]).transpose()
    print("created_aggregated_matrix kamel\n", created_aggregated_matrix)


    #here i'll be using a function to calculate the flots
    print("flowscreated_aggregated_matrix")
    differencesflots = calculateflows(created_aggregated_matrix)
    print(differencesflots)


    alt = np.append(Alternatives, " ")
    duplicated = np.vstack([alt, created_aggregated_matrix.transpose()])
    #so far created_aggregated_matrix is transposed 


    # def remove_last_element(arr):
    #     return arr[np.arange(arr.size - 1)]
    # fachnhat = remove_last_element(fachnhat)

    talyabachtetsetef  = np.vstack([duplicated, differencesflots]).transpose()


    print("##############")
    with numpy.printoptions(threshold=numpy.inf):
        print(talyabachtetsetef[:-1,:])

    # Sort 2D numpy array by first column
    sortedArr = talyabachtetsetef[talyabachtetsetef[:,-1].argsort()]
    print('Sorted 2D Numpy Array')
    print("##############")
    with numpy.printoptions(threshold=numpy.inf):
        print(np.flipud(sortedArr))
    print("Final Sort is : ")
    print(sortedArr[:,0])  
    print("*************************************-******************************************")      
    final_sorted = sortedArr[:,0]
    print("count finale :", len(final_sorted))
    print("type{}".format(type(final_sorted)))
    out_array = numpy.array_str(final_sorted)
    print(type(out_array[1]))
    listin  = list(out_array)
    print("list", listin)
    list_np = []
    for i in out_array:
        list_np.append(i)
    print(list_np, 'list_np')    
    print("type  list", type(list_np[0]))
    print("*****testing******")
    hh = final_sorted.tolist()
    print("hh",hh)
    liza = []
    hay_3liya = []
    zero = 1
    for i in hh:
        if len(i) != 1:
            liza.append(i)
            hay_3liya.append(zero)
            zero = zero+1
    context['hh'] = hh
    context['liza'] = liza
    context['zero'] = hay_3liya
    print("liza", liza)
    print("typt",liza[2])
    if request.method == 'POST':
        doc_file=request.FILES.get('myfile')
        mat = np.loadtxt(doc_file,dtype = str, skiprows=0, delimiter=',')
        print("matric",mat)i try 
    context['mat'] = mat   
    html_template = loader.get_template( 'promethee_2_page.html' )
    return HttpResponse(html_template.render(context, request))
import itertools
def ahp_final(request):
    html_template = loader.get_template( 'ahp_final.html')
    context = {}
    # //                                                                                                                           //
    critere_comparison = {('CarachterisiqueVaccin', 'Posologie'): 3, ('CarachterisiqueVaccin', 'Cout'): 7, ('CarachterisiqueVaccin', 'EffetsSecondaire'): 3,
    ('Posologie', 'Cout'): 9, ('Posologie', 'EffetsSecondaire'): 1,
    ('Cout', 'EffetsSecondaire'): 1/7}
    criteria = ahpy.Compare('Criteria', critere_comparison, precision=3)
    print()
    print('raport of criteria')
    print()
    report = criteria.report(show=True)
    # //                                                                                                                          //
    print()
    print('Subcriteria of CarachterisiqueVaccin ')
    print()
    caracterisiqueVaccin_comparison = {('Type', 'Efficacite'): 1/5}
    print()
    print('Subcriteria of Posologie')
    print()
    posologie_comparisons = {('NBrDose', 'Age'): 2, ('NBrDose', 'Delais'): 5, ('NBrDose', 'Temps_d_effet'): 3,
    ('Age', 'Delais'): 2, ('Age', 'Temps_d_effet'): 2,
    ('Delaise', 'Temps_d_effet'): 1/2}
    print()
    print('Subcriteria of Cout ')
    print()
    cout_comparisons = {('Conservation', 'Prix'): 1/5}
    effets_secondaire_comparisons = {('sensibilité_au_point_injection','douleur_au_point_injection'):3,('sensibilité_au_point_injection','céphalées'):2,('sensibilité_au_point_injection','hyperthermie'):1/5,('sensibilité_au_point_injection','nausées'):2,('sensibilité_au_point_injection','fatigue'):3,
    ('douleur_au_point_injection','céphalées'):5,('douleur_au_point_injection','hyperthermie'):1,('douleur_au_point_injection','nausées'):3,('douleur_au_point_injection','fatigue'):1/5,
    ('céphalées','hyperthermie'):6,('céphalées','nausées'):1/7,('céphalées','fatigue'):1/3,
    ('hyperthermie','nausées'):3,('hyperthermie','fatigue'):5,
    ('nausées','fatigue'):1/2}
    # //                                                                                                                          //
    print()
    print('Vaccins ')
    print()
    vaccins = ('AstraZeneca','Sinovac','sputnik','Janssen','Pfizer','Moderna')
    vaccin_pairs = list(itertools.combinations(vaccins, 2))
    print()
    print('Vaccins pairs')
    print()
    print(vaccin_pairs)
    print(type(vaccin_pairs), len(vaccin_pairs))
    print()
    print('**************************************************************************************************** ')
    print()
    # //                                                                                                                          //
    # subcriteria with alternative :
    print("subcriteria with alternative :")
    print()
    print('**************************************************************************************************** ')
    print()
    print("I")
    type_values = (9, 9, 1, 1/2, 5, 1, 1/9, 1/9, 1/7, 1/9, 1/9, 1/7, 1/2, 5, 6)
    type_comparisons = dict(zip(vaccin_pairs, type_values))
    print(type_comparisons)
    print()
    print('**************************************************************************************************** ')
    print()
    print("II")
    effecacite_values = (1, 5, 7, 9, 1/3, 5, 7, 9, 1/3, 2, 9, 1/8, 2, 1/8, 1/9)
    effecacite_comparisons = dict(zip(vaccin_pairs, effecacite_values))
    print()
    print('**************************************************************************************************** ')
    print()
    print("III")
    nbr_dose_values = (1, 1/2, 1, 3, 1/2, 1/2, 1, 3, 1/2, 2, 6, 1, 3, 1/2, 1/6)
    nbr_dose_comparisons = dict(zip(vaccin_pairs, nbr_dose_values))
    print()
    print('**************************************************************************************************** ')
    print()
    print("IV")
    age_values = (1/1.13, 1.41, 1.15, 1.24, 1.19, 1.59, 1.3, 1.4, 1.35, 1/1.23, 1/1.14, 1/1.18, 1.08, 1.04, 1/1.04)
    age_comparisons = dict(zip(vaccin_pairs, age_values))
    print()
    print('**************************************************************************************************** ')
    print()
    print("V")
    delais_values = (3, 4, 1/2, 2, 2, 2, 1/5, 1, 1, 1/6, 1/2, 1/2, 4, 4, 1)
    delais_comparisons = dict(zip(vaccin_pairs, delais_values))
    print()
    print('**************************************************************************************************** ')
    print()
    print("VI")
    temps_effet_values = (1, 7, 5, 9, 6, 7, 5, 9, 6, 1/6, 3, 1/3, 7, 5, 1/5)
    temps_effet_comparisons = dict(zip(vaccin_pairs, temps_effet_values))
    print()
    print('**************************************************************************************************** ')
    print()
    print("VII")
    conservation_values = (1, 1/2, 1/2, 1/2, 1/3, 1/2, 1/2, 1/2, 1/3, 1, 1, 1/2, 1, 1/2, 1/2)
    conservation_comparisons = dict(zip(vaccin_pairs, conservation_values))
    print()
    print('**************************************************************************************************** ')
    print()
    print("VIII")
    prix_values = (9, 9, 1, 1/2, 5, 1, 1/9, 1/9, 1/7, 1/9, 1/9, 1/7, 1/2, 5, 6)
    prix_comparisons = dict(zip(vaccin_pairs, prix_values))
    print()
    print('**************************************************************************************************** ')
    print()
    print("IX")
    a_values = (9, 9, 1, 1/2, 5, 1, 1/9, 1/9, 1/7, 1/9, 1/9, 1/7, 1/2, 5, 6)
    b_comparisons = dict(zip(vaccin_pairs, a_values))
    print()
    print('**************************************************************************************************** ')
    print()
    print("X")
    sapi_values = (1, 1/2, 1, 3, 1/2, 1/2, 1, 3, 1/2, 2, 6, 1, 3, 1/2, 1/6)
    sapi_comparisons = dict(zip(vaccin_pairs, sapi_values))
    print('**************************************************************************************************** ')
    print()
    print("XI")
    dapi_values = (3, 4, 1/2, 2, 2, 2, 1/5, 1, 1, 1/6, 1/2, 1/2, 4, 4, 1)
    dapi_comparisons = dict(zip(vaccin_pairs, dapi_values))
    print()
    print('**************************************************************************************************** ')
    print()
    print("XII")
    cephalees_values = (1, 7, 5, 9, 6, 7, 5, 9, 6, 1/6, 3, 1/3, 7, 5, 1/5)
    cephalees_comparisons = dict(zip(vaccin_pairs, cephalees_values))
    print('**************************************************************************************************** ')
    print()
    print("XIII")
    hyperthermie_values = (1, 1/2, 1/2, 1/2, 1/3, 1/2, 1/2, 1/2, 1/3, 1, 1, 1/2, 1, 1/2, 1/2)
    hyperthermie_comparisons = dict(zip(vaccin_pairs, hyperthermie_values))
    print()
    print('**************************************************************************************************** ')
    print()
    print("XIV")
    nausées_values = (1, 1/2, 1, 3, 1/2, 1/2, 1, 3, 1/2, 2, 6, 1, 3, 1/2, 1/6)
    nausées_comparisons = dict(zip(vaccin_pairs, nausées_values))
    print('**************************************************************************************************** ')
    print()
    print("XV")
    fatigue_values = (9, 9, 1, 1/2, 5, 1, 1/9, 1/9, 1/7, 1/9, 1/9, 1/7, 1/2, 5, 6)
    fatigue_comparisons = dict(zip(vaccin_pairs, fatigue_values))
    print()
    print('**************************************************************************************************** ')
    print()
    # //                                                                                                                            //
    # add all cretiria and sub creteria to Compare object
    # I criteria :   CarachterisiqueVaccin, Posologie, Cout, EffetsSecondaire
    caracteristique_vacc = ahpy.Compare('CarachterisiqueVaccin', caracterisiqueVaccin_comparison, precision=3)
    posologie = ahpy.Compare('Posologie', posologie_comparisons, precision=3)
    cout = ahpy.Compare('Cout', cout_comparisons, precision=3)
    effait_sec = ahpy.Compare('EffetsSecondaire', effets_secondaire_comparisons, precision=3)
    # subcriteria
    # 
    type_s = ahpy.Compare('Type', type_comparisons, precision=3)
    efficacite = ahpy.Compare('Efficacite', effecacite_comparisons, precision=3)
    nbr_dose = ahpy.Compare('NBrDose', nbr_dose_comparisons, precision=3)
    age = ahpy.Compare('Age', age_comparisons, precision=3)
    delais = ahpy.Compare('Delais', delais_comparisons, precision=3)
    temp_eff = ahpy.Compare('Temps_d_effet', temps_effet_comparisons, precision=3)
    conservation = ahpy.Compare('Conservation', conservation_comparisons, precision=3)
    prix = ahpy.Compare('Prix', prix_comparisons, precision=3)
    # 
    sapi = ahpy.Compare('sensibilité_au_point_injection', type_comparisons, precision=3)
    dapi = ahpy.Compare('douleur_au_point_injection', type_comparisons, precision=3)
    cephalees = ahpy.Compare('céphalées', dapi_comparisons, precision=3)
    hyperthermie = ahpy.Compare('hyperthermie', hyperthermie_comparisons, precision=3)
    nausees = ahpy.Compare('nausées', nausées_comparisons, precision=3)
    fatigue = ahpy.Compare('fatigue', fatigue_comparisons, precision=3)

    # link all comparte object in hearchy
    caracteristique_vacc.add_children([type_s,efficacite])
    posologie.add_children([nbr_dose,age,delais,temp_eff])
    cout.add_children([conservation,prix])
    effait_sec.add_children([sapi,dapi,cephalees,hyperthermie,nausees,fatigue])
    criteria.add_children([caracteristique_vacc,posologie,cout,effait_sec])
    print()
    print(criteria.target_weights)
    print()
    result = criteria.target_weights
    keys = []
    values = []
    for key, val in result.items():
        keys.append(key)
        values.append(val)
    context['final'] = criteria.target_weights
    context['keys'] = keys
    context['values'] = values
    return HttpResponse(html_template.render(context, request))    





   
    
    


