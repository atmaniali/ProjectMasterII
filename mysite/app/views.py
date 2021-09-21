# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from typing import ContextManager
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
            messages.success(request, "Votre compte {} et bien modifier".format(request.user.username))
            form.save()
            return redirect("app:profile")

        else:
            messages.error(request, "votre compte n'est pas modifier")  

    context['form'] = form
    context['segment'] = 'profile'

    html_template = loader.get_template( 'profile.html' )
    return HttpResponse(html_template.render(context, request))      
    
      
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
      


def promether_view(request) :

    context = {}

    if 'envoyer' in request.POST:
        doc_file=request.FILES.get('myfile')
        weight_file = request.FILES.get('myfile1')
        mat = np.loadtxt(doc_file,dtype = str, skiprows=0, delimiter=',')      
        context['mat'] = mat  
        result_alter , poursen = readMatrix(doc_file, weight_file) 
        lentgh = len(poursen)
        print (poursen)
        result_poursen = get_weight(poursen)
        if lentgh != 0:
            dict = {}
            for i in range(lentgh - 1):
                keys = result_alter[i]
                dict[keys] = round(result_poursen[i], 2)

            context['dict'] = dict
        context['result'] = result_alter  
        context ['poursentage'] = result_poursen
    elif 'annuler' in request.POST:
        return redirect('app:home') 

    html_template = loader.get_template( 'promethee_2_page.html' )

    return HttpResponse(html_template.render(context, request))


def ahp_final(request):

    html_template = loader.get_template( 'ahp_final.html')
    context = {}
    if 'ahp_crit_sui' in request.POST:
        critere_file = request.FILES.get('critere')
        mat = np.loadtxt(doc_file,dtype = str, skiprows=0, delimiter=',')
        critere_filecsv = from_csv_to_dict(critere_file) 
        critere_comparison = critere_filecsv 
        print(critere_comparison)
        criteria = ahpy.Compare('Criteria', critere_comparison, precision=3)
        criteria_result = criteria.target_weights
        keys = criteria_result.keys()
        values = criteria_result.values()
        values = list(values)
        keys = list(keys)   
        context['mat'] = mat 
        context['criteria_result'] = criteria_result 
        context['keys'] = keys
        context['values'] = values
    elif 'ahp_crit_ann' in request.POST   :
        return redirect("app:home") 

    elif 'ahp_crit_ann2' in request.POST   :
        return redirect("app:home")  
    elif 'ahp_crit_sui2' in request.POST: 
        test = ['yes','yes']
        keys, values = ahp_finales()
        context['x'] = keys
        context['y'] = values  
        context['test']  = test  
    #     critere_file = request.FILES.get('critere')
    #     caracteristique_vaccin_file = request.FILES.get('caracteristique_vaccin')
    #     posologie_file = request.FILES.get('posologie')
    #     cout_file = request.FILES.get('cout')
    #     effets_secondaire_file = request.FILES.get('effets_secondaire')
    #     # tuple
    #     alternatives_file = request.FILES.get('alternatives')
    #     type_file = request.FILES.get('type')
    #     efficacite_file = request.FILES.get('efficacite')
    #     nbr_dose_file = request.FILES.get('nbr_dose')
    #     age_file = request.FILES.get('age')
    #     delais_file = request.FILES.get('delais')
    #     temps_effet_file = request.FILES.get('temps_effet')
    #     conservation_file = request.FILES.get('conservation')
    #     prix_file = request.FILES.get('prix')
    #     sen_au_point_file = request.FILES.get('sen_au_point')
    #     doul_au_point_file = request.FILES.get('doul_au_point')
    #     cephales_file = request.FILES.get('cephales')
    #     hyperthermie_file = request.FILES.get('hyperthermie')
    #     nausees_file = request.FILES.get('nausees')
    #     fatigue_file = request.FILES.get('fatigue')
    #     # csv_to_dictionaire
    #     critere_filecsv = from_csv_to_dict(critere_file)
    #     caracteristique_vaccin_filecsv = from_csv_to_dict(caracteristique_vaccin_file)
    #     posologie_filecsv = from_csv_to_dict(posologie_file)
    #     cout_filecsv = from_csv_to_dict(cout_file)
    #     effets_secondaire_filecsv = from_csv_to_dict(effets_secondaire_file)
    #     # csv_to_tuple
    #     alternatives_filecsv = from_csv_to_tuple(alternatives_file,str)
    #     type_filecsv = from_csv_to_tuple(type_file,float)
    #     efficacite_filecsv = from_csv_to_tuple(efficacite_file,float)
    #     nbr_dose_filecsv = from_csv_to_tuple(nbr_dose_file,float)
    #     age_filecsv = from_csv_to_tuple(age_file,float)
    #     delais_filecsv = from_csv_to_tuple(delais_file,float)
    #     temps_effet_filecsv  = from_csv_to_tuple(temps_effet_file,float)
    #     conservation_filecsv = from_csv_to_tuple(conservation_file,float)
    #     prix_filecsv = from_csv_to_tuple(prix_file,float)
    #     sen_au_point_filecsv = from_csv_to_tuple(sen_au_point_file,float)
    #     doul_au_point_filecsv = from_csv_to_tuple(doul_au_point_file,float)
    #     cephales_filecsv = from_csv_to_tuple(cephales_file,float)
    #     hyperthermie_filecsv = from_csv_to_tuple(hyperthermie_file,float)
    #     nausees_filecsv = from_csv_to_tuple(nausees_file,float)
    #     fatigue_filecsv = from_csv_to_tuple(fatigue_file,float)
    #     # start methode 
    #     critere_comparison = critere_filecsv
    #     criteria = ahpy.Compare('Criteria', critere_comparison, precision=3)
    #     print("criteria \n",criteria.target_weights)
    #     caracterisiqueVaccin_comparison = caracteristique_vaccin_filecsv
    #     posologie_comparisons = posologie_filecsv
    #     cout_comparisons = cout_filecsv
    #     effets_secondaire_comparisons = effets_secondaire_filecsv
    #     vaccins = alternatives_filecsv
    #     vaccin_pairs = list(itertools.combinations(vaccins, 2))
    #     type_values = type_filecsv
    #     type_comparisons = dict(zip(vaccin_pairs, type_values))
    #     effecacite_values = efficacite_filecsv
    #     effecacite_comparisons = dict(zip(vaccin_pairs, effecacite_values))
    #     nbr_dose_values = nbr_dose_filecsv
    #     nbr_dose_comparisons = dict(zip(vaccin_pairs, nbr_dose_values))
    #     age_values = age_filecsv 
    #     age_comparisons = dict(zip(vaccin_pairs, age_values))
    #     delais_values = delais_filecsv
    #     delais_comparisons = dict(zip(vaccin_pairs, delais_values))
    #     temps_effet_values = temps_effet_filecsv
    #     temps_effet_comparisons = dict(zip(vaccin_pairs, temps_effet_values))
    #     conservation_values = conservation_filecsv
    #     conservation_comparisons = dict(zip(vaccin_pairs, conservation_values))
    #     prix_values = prix_filecsv 
    #     prix_comparisons = dict(zip(vaccin_pairs, prix_values))
    #     sapi_values = sen_au_point_filecsv
    #     sapi_comparisons = dict(zip(vaccin_pairs, sapi_values))
    #     dapi_values = doul_au_point_filecsv 
    #     dapi_comparisons = dict(zip(vaccin_pairs, dapi_values))
    #     print("dapi_comparisons \n",dapi_comparisons)
    #     cephalees_values = cephales_filecsv
    #     cephalees_comparisons = dict(zip(vaccin_pairs, cephalees_values))
    #     hyperthermie_values = hyperthermie_filecsv
    #     hyperthermie_comparisons = dict(zip(vaccin_pairs, hyperthermie_values))
    #     nausées_values = nausees_filecsv
    #     nausées_comparisons = dict(zip(vaccin_pairs, nausées_values))
    #     fatigue_values = fatigue_filecsv 
    #     fatigue_comparisons = dict(zip(vaccin_pairs, fatigue_values))
    #     caracteristique_vacc = ahpy.Compare('CarachterisiqueVaccin', caracterisiqueVaccin_comparison, precision=3)
    #     posologie = ahpy.Compare('Posologie', posologie_comparisons, precision=3)
    #     print("posologie \n",posologie.target_weights)
    #     cout = ahpy.Compare('Cout', cout_comparisons, precision=3)
    #     effait_sec = ahpy.Compare('EffetsSecondaire', effets_secondaire_comparisons, precision=3)
    #     type_s = ahpy.Compare('Type', type_comparisons, precision=3)
    #     efficacite = ahpy.Compare('Efficacite', effecacite_comparisons, precision=3)
    #     nbr_dose = ahpy.Compare('NBrDose', nbr_dose_comparisons, precision=3)
    #     age = ahpy.Compare('Age', age_comparisons, precision=3)
    #     delais = ahpy.Compare('Delais', delais_comparisons, precision=3)
    #     temp_eff = ahpy.Compare('Temps_d_effet', temps_effet_comparisons, precision=3)
    #     conservation = ahpy.Compare('Conservation', conservation_comparisons, precision=3)
    #     prix = ahpy.Compare('Prix', prix_comparisons, precision=3)
    #     sapi = ahpy.Compare('sensibilité_au_point_injection', sapi_comparisons, precision=3)
    #     dapi = ahpy.Compare('douleur_au_point_injection', dapi_comparisons, precision=3)
    #     cephalees = ahpy.Compare('céphalées', cephalees_comparisons, precision=3)
    #     hyperthermie = ahpy.Compare('hyperthermie', hyperthermie_comparisons, precision=3)
    #     nausees = ahpy.Compare('nausées', nausées_comparisons, precision=3)
    #     fatigue = ahpy.Compare('fatigue', fatigue_comparisons, precision=3)
    #     print("fatigue \n", fatigue.target_weights)
    #     print("fatigue type \n", type(fatigue.target_weights))
    #    # link all comparte object in hearchy
    #     caracteristique_vacc.add_children([type_s,efficacite])
    #     posologie.add_children([nbr_dose,age,delais,temp_eff])
    #     cout.add_children([conservation,prix])
    #     effait_sec.add_children([sapi,dapi,cephalees,hyperthermie,nausees,fatigue])
    #     criteria.add_children([caracteristique_vacc,posologie,cout,effait_sec])
    #     print("cr", criteria)
    #     print("final criteria \n", criteria.target_weights)
        
    return HttpResponse(html_template.render(context, request))  

def maps (request):
    template_name = "maps.html"
    context = {}
    ip = "193.194.88.26"
    #
    map = folium.Map(width = 800, height = 500, location = [35.6976541, -0.6337376], zoom_start = 7)
    # all provinces
    provinces = get_all_provinces()

    for province in provinces:
        for data in province['data'] : 
            folium.Marker([province['latitude'], province['longitude']], tooltip = "click here for more", popup = "nom de wilaya: {} confirmed is: {}".format(province['name'], data["confirmed"]), icon = folium.Icon(color= 'purple')).add_to(map) 
        
    map = map._repr_html_() 
    context["maps"] = map
    return render(request, template_name, context)      


# Methode I


def shows(request):
    template_name = "show.html"
    context = {}
    # All
   
    criters = Subcritere.objects.all()
             
    alternatives = Alternative.objects.all()
    if 'check_box' in request.POST:    
        # get List of Critere Alternative cheking
        crits = request.POST.getlist('crits')
        alti = request.POST.getlist('alts')

        if len(crits) != 0 and len(alti) != 0:
            x = len(crits)
            y = len(alti)
            # Save taille of list for create matrix
            taille = Taille.objects.create(rows = x, colmn = y)  
            taille.save()

            messages.success(request,"succes")
            # Create matrix de perfermance
            mat = get_matrix(crits, alti)
            # Create list of weight
            wei = get_list(crits)

            context["matrix"] = mat
            context["weights"] = wei

        elif len(crits) == 0:
            messages.error(request, "check critere one or more !")
        elif len(alti) == 0 :
            messages.error(request, "check Altirnative one or more !")    
    # get MP and weight
    elif 'tabl'  in request.POST: 
        # get  list of rows
        tab = request.POST.getlist("cells")
        mp_names = request.POST.get('mp_names')
        
        # get list of weight
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
            user = request.user.id 
            profile = Profile.objects.get(user = user)
            # weight_to_csv(weight_numpy,weight_names, profile)
            numpy_to_csv(matrix, mp_names, profile, weight_numpy)  
    elif 'tablCancel' in request.POST : 
        return redirect('app:home')        
      
    context["criters"] = criters
    context["alternatives"] = alternatives
    return render(request, template_name, context)

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
def listes(request):

    template_name = "listes.html"
    context = {}

    criters = Critere.objects.all().order_by('pk')
    
    if 'add' in request.POST :
        name = request.POST.get('is')
        id  = request.POST.get('id')
        critere = get_object_or_404(Critere, pk=int(id)) 
        critere.name = name
        critere.save()
    if 'delete' in request.POST :
        id  = request.POST.get('id') 
        critere = get_object_or_404(Critere, pk=int(id)) 
        critere.delete()
    if 'addAlternatve' in request.POST:
        name = request.POST.get('is')
        id  = request.POST.get('id_alt')
        print(request.POST) 
        alternative = get_object_or_404(Alternative, pk=int(id))
        alternative.nom_vaccin = name 
        alternative.save()
    if 'deleteAlternative' in request.POST:   
        name = request.POST.get('is')
        id  = request.POST.get('id_del')
        print(request.POST) 
        alternative = get_object_or_404(Alternative, pk=int(id)) 
        alternative.delete()
    if 'addSub' in request.POST:
        id  = request.POST.get('id_sub')
        sub = get_object_or_404(Subcritere, pk=int(id))
        name = request.POST.get('is')
        select = request.POST.get("cri_sous")
        sub = get_object_or_404(Subcritere, pk=int(id))
        crit = get_object_or_404(Critere, pk=int(select))
        sub.name = name
        sub.critere = crit
        sub.save()
    if 'deleteSub' in request.POST:
        id  = request.POST.get('id_del')
        print(request.POST) 
        sub = get_object_or_404(Subcritere, pk=int(id)) 
        sub.delete()
          
        
    paginator_crit = Paginator(criters, 5)
    page = "request.GET.get('page', 1)"
    try:
        crits_paginater = paginator_crit.page(page)
    except PageNotAnInteger:
        crits_paginater = paginator_crit.page(1)
    except EmptyPage:
        crits_paginater = paginator_crit.page(paginator_crit.num_pages)
    alternatives = Alternative.objects.all()
    subcriters = Subcritere.objects.order_by('critere') 
    paginator_alti = Paginator(alternatives, 5)

    context["criteres"] = criters
    context['altirnatives'] = alternatives
    context["subcriters"] = subcriters
    context["paginator_crit"] = crits_paginater
    context['paginator_alti'] = paginator_alti 
    

    return render(request, template_name, context)


"""list str to list int"""
def list_str_to_int(lists):
    for i in range(len(lists)):
        lists[i] = int(lists[i])
    return lists    

"""take list of int and turn in queryset"""
def get_queryset(lists):
    listes = []
    for li in lists:
        b = Critere.objects.get(pk = li)
        listes.append(b)
    return listes

# deg get_name(lists):

"""turn criter and subcriter"""  
def get_cri_et_sub(lists):
    d = []    
    for i in lists:
        s = i.get_subcriters()
        z = s.split(',')
        if len(z) ==0:
            z = ''     
        case= {'critere':i.name, 'subcritere': z}
        d.append(case)     
    return d 
""" store names """    
def get_names(lists):
    for i in lists:
        Traveille.objects.create(name = i.name)
               


def show_sub(request):  
    template_name = "show_sub.html"  
    context = {}
    sub_cris = None
    criters = Critere.objects.all()
    if 'check_box' in request.POST:
        # list of critere id
        crits = request.POST.getlist('crits')

        if len(crits) != 0:
            messages.success(request,"succes critere")
            x = len(crits)
            taille_cri = Taille_sub.objects.create(rows = x)
            tab = list_str_to_int(crits)
            criters_2 = get_queryset(tab)
            # get dectionnaire of criteria and sub criteria
            cri_sub = get_cri_et_sub(criters_2)
            get_names(criters_2)
            print("cri_sub", cri_sub)
            
            alternatives = Alternative.objects.all()
            context["alternatives"] = alternatives
            context["cri_2"] = criters_2
            context["sub_cris"]= cri_sub
            sub_cris = sub_cris
        elif len(crits) == 0:
            messages.error(request, "check critere one or more !")
    elif 'check_box_all' in request.POST:
        subs = request.POST.getlist('i_sub')
        cr= []
        if len(subs) == 0:
            messages.error(request, "check subcritere one or more !")
        elif len(subs) != 0: 
            messages.success(request,"succes subcritere")   
            crits = Traveille.objects.all()
            for i in crits:
                cr.append(i.name)
            crits.delete()    
            mat_cri = get_matrix_ahp(cr, cr)
            mat_sub = get_matrix_ahp(subs, subs)
            context['mat_cri'] = mat_cri
            context['mat_sub'] = mat_sub
            context['yes'] = "yes"
    elif 'check_box_all_cancel' in  request.POST:  
        return redirect("app:home")
    elif 'tablcancel_cr'   in  request.POST:
        return redirect("app:home")
    elif 'tabl'  in request.POST:
        mp_names = request.POST.get('mp_names')
        tab = request.POST.getlist('cells') 
        tab_np = np.array(tab)  
        taille = Taille_sub.objects.all().last() 
        x = taille.rows+1
        tabl_np = np.reshape(tab_np,(x, x))
        user = request.user.id 
        profile = Profile.objects.get(user = user)
        numpy_to_csv_ahp(tabl_np,mp_names,profile)

    context["criters"] = criters
    return render(request, template_name, context)      


def add_critere(request):
    template_name = "addcritere.html"
    context = {}
    # form = CritereCritere(request.POST or None)
    # if request.method == 'POST':
    #     print(request.POST)
    #     print(request.user.id)
    #     if form.is_valid():
    #         critere = form.save(commit = False)
    #         critere.user = request.user 
    #         critere.save()   
    #         return redirect('app:critere_list')
           
    # context['form'] = form      
    return render(request, template_name, context)

def show_csv(request):
    template_name = "show_csv.html"
    context = {}
    csv_f = Upload_csv.objects.all()
    context["csv"] = csv_f
    if request.method  == "POST":
        id = request.POST.get("csv_name")
        print(id)
        obj = get_object_or_404(Upload_csv, pk = id)
        mp_path = obj.path
        weight_path = obj.path_weight
        context['url'] = obj       
        Matrix = np.loadtxt(mp_path,dtype = str, skiprows=0, delimiter=',')
        # Mat = np.loadtxt(weight_path,dtype = str, skiprows=0, delimiter=',')
        array_Matrix  = np.array(Matrix)
        mat_header  = array_Matrix[0]  
        mat_body = array_Matrix[2:]  
        # array_Mat  = np.array(Mat)
        context['array_Matrix_header'] = mat_header
        context['array_Matrix_body'] = mat_body
        # context['array_Mat'] = array_Mat
        
    return render(request, template_name, context)        
def get_id(request, id):
    template_name  = 'ahp_chart1.html'
    context= {'id ' : id}
    return render(request, template_name, context)




 


   
    
    


