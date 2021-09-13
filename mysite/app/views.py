# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from django.views import generic
from django.views.generic import ListView
from datetime import datetime
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
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
import folium
from django.contrib import messages

""" 
    all data from these url : https://api.corona-dz.live/
"""

# index 
@login_required(login_url="/login/")
def index(request):
    # Json file:

    # Getting all cases by gender data.
    all_genders = requests.get('https://api.corona-dz.live/country/gender/all').json()
    # Getting all amount of total confirmed cases, deaths, and recovered.
    all_country = requests.get('https://api.corona-dz.live/country/all').json()
    # Getting latest amount of total confirmed cases, deaths, and recovered.
    data = requests.get('https://api.corona-dz.live/country/latest').json()
    # Getting latest data for cases by age.
    latest_age = requests.get('https://api.corona-dz.live/country/age/latest').json()

    # Date of latest data
    date_auj = parse_datetime(data['date']).date()

    # Tables for stock data from Json file:

    males = []    #stock all latest confirmed gender male => from all_genders.
    females = []    #stock all latest confirmed gender femal => from all_genders.
    confirmedes = []    #stock all confirmedfrom country.
    dates_all_genderes = []    #stock all date of all gender.

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

    id = 31
    if request.method == 'POST':
        " this methode for print data of wilaya givin by id"
        id = request.POST.get('wilaya')
        
    urls = "https://api.corona-dz.live/province/{}/latest".format(id)
    wilaya_data = requests.get(urls).json()
    result = wilaya_data[0] #json data in index 1
    final_result = result['data'] 
        
    # pass data to templates
        
    context['wilaya'] = final_result[0] #json data in index 1
    context['males'] = males[-6:] #latest of 6 index male confirmed.
    context['females'] = females [-6:]  #latest of 6 index female confirmed. 
    context['date_all'] = dates_all_genderes [-6:]  #pass all date 
    context['latest_age'] = latest_age  #pass all age data.
    context['confirmedes'] = confirmedes[-6:]   #pass all confirmedes data
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
    context  = {}
    context['segment'] = 'home' 

    html_template = loader.get_template( 'home.html' )
    return HttpResponse(html_template.render(context, request)) 

# profile
@login_required(login_url="/login/")
def profile(request):

    context = {}
    # stock information of user if exist in form
    form = ContactForm(request.POST or None, instance= request.user.profile)

    if request.method =='POST':
        
        if form.is_valid():

            form.save()
            return redirect("app:profile")

        else:
            print("request not pass ")  

    context['form'] = form
    context['segment'] = 'profile'

    html_template = loader.get_template( 'profile.html' )
    return HttpResponse(html_template.render(context, request))      
    
    
       
def create_critere_normal(request):
    """create multiple critere and show in tables"""

    template_name = 'create_critere_normal.html'
    heading_message = 'Create critere'    
    context = {}

    if request.method == 'GET':

        formset = CritereFormset(request.GET or None)

    elif request.method == 'POST':
        formset = CritereFormset(request.POST)
        if formset.is_valid():
            # recupirer le nom de fichier
            csv_file = request.POST.get('input_name')
            for form in formset:
                name = form.cleaned_data.get('name')
                # save Critere instance
                if name:    
                    Critere(name=name).save()
            # if non text cauz err
            if len(csv_file ) != 0 :

                # get all critere.
                query = Critere.objects.all()
                # stock critere name.
                list_critere = []

                for i in query:
                    list_critere.append(i.name) 
                # turn into ndarray   
                list_np = np.array(list_critere) 
                # matrix null
                matrix = [ [ 0 for i in range(len(list_np)) ] for j in range(len(list_np)) ]

                for i in range(len(list_np)):
                    for j in range(len(list_np)):
                        # diagonale
                        if i == j:
                            matrix[i][j] = 1

                    matrix_np = np.array(matrix) 

                    # add critere name in matrix
                    matrix_with_critere_ligne= np.vstack((list_np,matrix_np))

                    matrix_transpose = matrix_with_critere_ligne.transpose()
                    list_np_1 = np.append("",list_np) #append first element "".
                    matrix_with_critere_ligne_transpose= np.vstack((list_np_1,matrix_transpose))
                    #turn into data frame.
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
        # Add in a QuerySet of all the subcriteres
        context['subcritere_list'] = Subcritere.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            if request.POST.get('te') :
                # te is id pass with ajax
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

        critereform = CritereModelForm(request.GET or None)

        formset = SubcritereFormset(queryset=Subcritere.objects.none())

    elif request.method == 'POST':

        critereform = CritereModelForm(request.POST)
        
        formset = SubcritereFormset(request.POST)
        
        if critereform.is_valid() and formset.is_valid():
            
            # first save this critere, as its reference will be used in `subcritere`
            critere = critereform.save()
            for form in formset:
                # so that `critere` instance can be attached.
                subcritere = form.save(commit=False)
                subcritere.critere = critere
                subcritere.save()
            return redirect('app:critere_list')
    return render(request, template_name, {
        'critereform': critereform,
        'formset': formset,
    }) 
            
def promether_view(request) :

    context = {}

    if request.method == 'POST':
        doc_file=request.FILES.get('myfile')
        weight_file = request.FILES.get('myfile1')
        mat = np.loadtxt(doc_file,dtype = str, skiprows=0, delimiter=',')      
        context['mat'] = mat  
        result_alter , poursen = readMatrix(doc_file, weight_file) 
        result_poursen = get_weight(poursen)

        context['result'] = result_alter  
        context ['zero'] = result_poursen

    html_template = loader.get_template( 'promethee_2_page.html' )

    return HttpResponse(html_template.render(context, request))


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
        result = criteria.target_weights
        # print(criteria.target_weights)
        
        for key, val in result.items():
            keys.append(key)
            values.append(val)
        context['final'] = criteria.target_weights
        context['keys'] = keys
        context['values'] = values
    x = ['Moderna', 'AstraZeneca', 'Sinovac', 'Janssen', 'Pfizer', 'sputnik']
    y = [0.279, 0.208, 0.153, 0.138, 0.122, 0.099]
    context['x'] = x
    context['y'] = y
    return HttpResponse(html_template.render(context, request))  

def maps (request):
    template_name = "maps.html"
    context = {}
    ip = "193.194.88.26"
    #
    map = folium.Map(width = 800, height = 500, location = [35.6976541, -0.6337376], zoom_start = 8)
    # all provinces
    provinces = get_all_provinces()

    for province in provinces:
        for data in province['data'] : 
            folium.Marker([province['latitude'], province['longitude']], tooltip = "click here for more", popup = "nom de wilaya {} confirmed is {}:".format(province['name'], data["confirmed"]), icon = folium.Icon(color= 'purple')).add_to(map) 
        
    map = map._repr_html_() 
    context["maps"] = map
    return render(request, template_name, context)      


# Methode I

def creating (request) : 
    
    context = {}
    template_name = "creating.html"
    heading_message = 'Create Alternatives and Critere '      
    if request.method == 'GET':
        formset = AlternativeModelFormset(request.GET or None)
        formset2 = CritereModelFormset(request.GET or None)
    elif request.method == 'POST':
        formset = AlternativeModelFormset(request.POST)
        formset2 = CritereModelFormset(request.POST)
        if 'alternative' in request.POST:
            if formset.is_valid():
                for form in formset:
                    print("form",form) 
                    if form.cleaned_data.get('name'):
                        form.save()
                    
                    return redirect('app:creating')    
        if 'critere' in request.POST:                
            if formset2.is_valid():
                for form2 in formset2:
                    name = form2.cleaned_data.get('name')  
                    if name:
                        Critere(name = name).save()          
                # once all alternatives are saved, redirect to alternative list view
                return redirect('app:creating')
                
    return render(request, template_name, {
        'formset': formset,
        'formset2': formset2,
        'heading': heading_message,
    }) 


def shows(request):
    template_name = "show.html"
    context = {}
    # All
    criters = Critere.objects.all()
    alternatives = Alternative.objects.all()
    if 'check_box' in request.POST:
        
        print(request.POST)
        crits = request.POST.getlist('crits')
        alti = request.POST.getlist('alts')
        if len(crits) != 0 and len(alti) != 0:
            x = len(crits)
            y = len(alti)
            taille = Taille.objects.create(rows = x, colmn = y)  
            taille.save()
            messages.success(request,"succes")
            mat = get_matrix(crits, alti)
            wei = get_list(crits)
            context["matrix"] = mat
            context["weights"] = wei
        elif len(crits) == 0:
            messages.error(request, "check critere one or more !")
        elif len(alti) == 0 :
            messages.error(request, "check Altirnative one or more !")    
    
    elif 'tabl'  in request.POST: 
        tab = request.POST.getlist("cells")
        weight = request.POST.getlist("weights")
        weight_numpy = np.array(weight).astype(float)
        summs = np.sum(weight_numpy)
        taille = Taille.objects.all().last()   
        tab_np = np.array(tab)  
        x = taille.colmn+1
        y = taille.rows+1
        tabl_np = np.reshape(tab_np,(x, y))
        matrix = slicing(tabl_np)
        if summs <= 0:
            messages.info(request,"weight should be > 0")
        elif summs > 1:
            messages.info(request,"weight should be > 0")
        else :   
            messages.success(request, "success")   
            weight_to_csv(weight_numpy,"name_weight")
        numpy_to_csv(matrix, "name")
        
    # table = [
    # ['', 'Foo', 'Bar', 'Barf'],
    # ['Spam', 101, 102, 103],
    # ['Eggs', 201, 202, 203],] 
    # test = ['test','yes','no','yes']
      
    
    context["criters"] = criters
    context["alternatives"] = alternatives
    # context['table'] = table
    
       
    return render(request, template_name, context)

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
def listes(request):
    template_name = "listes.html"
    context = {}
    criters = Critere.objects.all().order_by('pk')
    paginator_crit = Paginator(criters, 5)
    page = "request.GET.get('page', 1)"
    try:
        crits_paginater = paginator_crit.page(page)
    except PageNotAnInteger:
        crits_paginater = paginator_crit.page(1)
    except EmptyPage:
        crits_paginater = paginator_crit.page(paginator_crit.num_pages)
    alternatives = Alternative.objects.all()
    subcriters = Subcritere.objects.all()
    paginator_alti = Paginator(alternatives, 5)

    context["criteres"] = criters
    context['altirnatives'] = alternatives
    context["subcriters"] = subcriters
    context["paginator_crit"] = crits_paginater
    context['paginator_alti'] = paginator_alti 

    return render(request, template_name, context)

def creating_sub(request):
    template_name = "creating_sub.html"
    context = {}
    return render(request, template_name, context)

"""list str to list int"""
def list_str_to_int(lists):
    for i in range(len(lists)):
        lists[i] = int(lists[i])
    return lists    

"""take list of int and turn in queryset"""
def get_queryset(lists):
    z = []
    for li in lists:
        b = Critere.objects.get(pk = li)
        z.append(b)
    return z 

"""get all subcritere """  
def get_sub_crit(lists):
    crrr = []
    for li in lists:
        cr = Critere.objects.get(pk = li)
        crr = cr.subcriters.all()
        crrr.append(crr)
    return(crrr)

"""test query set if vide""" 
def get_taille(lists):
    necr = []
    for li in lists:
        if li.count()!= 0:
            necr.append(li)
    return necr 

""" get query to name"""
def get_name_sub(listes):
    tabs = []
    for i in listes:
        for j in i:
            tabs.append(j.name)
    return tabs 

"""turn criter and subcriter"""  
def get_cri_et_sub(lists):
    d = []
    for i in lists:
        z = i.get_subcriters()
        if len(z) ==0:
            z = ''
        case= {'critere':i.name, 'subcritere': z}
        d.append(case) 
    return d   


def show_sub(request):  
    template_name = "show_sub.html"  
    context = {}
    criters = Critere.objects.all()
    if 'check_box' in request.POST:
        crits = request.POST.getlist('crits')
        if len(crits) != 0:
            messages.success(request,"succes")
            tab = list_str_to_int(crits)
            criters_2 = get_queryset(tab)
            print(criters_2)
            cri_sub = get_cri_et_sub(criters_2)
            alternatives = Alternative.objects.all()
            context["alternatives"] = alternatives
            context["cri_2"] = criters_2
            context["sub_cris"]= cri_sub

        elif len(crits) == 0:
            messages.error(request, "check critere one or more !")
  
    

    context["criters"] = criters
    return render(request, template_name, context)      






   
    
    


