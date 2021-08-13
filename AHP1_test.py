from ahpy import ahpy
import itertools
import numpy as np
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
# dictionnaire
critere_file = "/home/ali/Documents/MasterIIproect/ahp_csv_all/criter.csv"
caracteristique_vaccin_file = "/home/ali/Documents/MasterIIproect/ahp_csv_all/sub_critere_caractiristique_vaccin.csv"
posologie_file = "/home/ali/Documents/MasterIIproect/ahp_csv_all/sub_critere_posologie.csv"
cout_file = "/home/ali/Documents/MasterIIproect/ahp_csv_all/sub_critere_cout.csv"
effets_secondaire_file = "/home/ali/Documents/MasterIIproect/ahp_csv_all/sub_critere_effect_secondaire.csv"
alternatives_file = "/home/ali/Documents/MasterIIproect/ahp_csv_all/alternative.csv"
type_file = "/home/ali/Documents/MasterIIproect/ahp_csv_all/type.csv"
efficacite_file = "/home/ali/Documents/MasterIIproect/ahp_csv_all/effecacite.csv"
nbr_dose_file = "/home/ali/Documents/MasterIIproect/ahp_csv_all/nbr_dose.csv"
age_file = "/home/ali/Documents/MasterIIproect/ahp_csv_all/age.csv"
delais_file = "/home/ali/Documents/MasterIIproect/ahp_csv_all/delais.csv"
temps_effet_file = "/home/ali/Documents/MasterIIproect/ahp_csv_all/temps_effet.csv"
conservation_file = "/home/ali/Documents/MasterIIproect/ahp_csv_all/conservation.csv"
prix_file = "/home/ali/Documents/MasterIIproect/ahp_csv_all/prix.csv"
sen_au_point_file = "/home/ali/Documents/MasterIIproect/ahp_csv_all/sapi.csv"
doul_au_point_file = "/home/ali/Documents/MasterIIproect/ahp_csv_all/delais.csv"
cephales_file = "/home/ali/Documents/MasterIIproect/ahp_csv_all/cephalees.csv"
hyperthermie_file = "/home/ali/Documents/MasterIIproect/ahp_csv_all/hyperthermie.csv"
nausees_file = "/home/ali/Documents/MasterIIproect/ahp_csv_all/nause.csv"
fatigue_file = "/home/ali/Documents/MasterIIproect/ahp_csv_all/fatigue.csv"
# csv_to_dictionaire
critere_filecsv = from_csv_to_dict(critere_file)
print("critere_filecsv",critere_filecsv)
caracteristique_vaccin_filecsv = from_csv_to_dict(caracteristique_vaccin_file)
print("caracteristique_vaccin_filecsv",caracteristique_vaccin_filecsv)
posologie_filecsv = from_csv_to_dict(posologie_file)
print("posologie_filecsv",posologie_filecsv)
cout_filecsv = from_csv_to_dict(cout_file)
print("cout_filecsv",cout_filecsv)
effets_secondaire_filecsv = from_csv_to_dict(effets_secondaire_file)
print("effets_secondaire_filecsv",effets_secondaire_filecsv)
# csv_to_tuple
alternatives_filecsv = from_csv_to_tuple(alternatives_file,str)
print("alternatives_filecsv",alternatives_filecsv)
type_filecsv = from_csv_to_tuple(type_file,float)
print("type_filecsv",type_filecsv )
efficacite_filecsv = from_csv_to_tuple(efficacite_file,float)
print("efficacite_filecsv",efficacite_filecsv )
nbr_dose_filecsv = from_csv_to_tuple(nbr_dose_file,float)
print("nbr_dose_filecsv",nbr_dose_filecsv )
age_filecsv = from_csv_to_tuple(age_file,float)
print("age_filecsv",age_filecsv )
delais_filecsv = from_csv_to_tuple(delais_file,float)
print("delais_filecsv",delais_filecsv )
temps_effet_filecsv  = from_csv_to_tuple(temps_effet_file,float)
print("temps_effet_filecsv ", temps_effet_filecsv )
conservation_filecsv = from_csv_to_tuple(conservation_file,float)
print("conservation_filecsv",conservation_filecsv )
prix_filecsv = from_csv_to_tuple(prix_file,float)
print("prix_filecsv ", prix_filecsv )
sen_au_point_filecsv = from_csv_to_tuple(sen_au_point_file,float)
print("sen_au_point_filecsv", sen_au_point_filecsv)
doul_au_point_filecsv = from_csv_to_tuple(doul_au_point_file,float)
print("doul_au_point_filecsv",doul_au_point_filecsv )
cephales_filecsv = from_csv_to_tuple(cephales_file,float)
print("cephales_filecsv",cephales_filecsv )
hyperthermie_filecsv = from_csv_to_tuple(hyperthermie_file,float)
print("hyperthermie_filecsv ",hyperthermie_filecsv )
nausees_filecsv = from_csv_to_tuple(nausees_file,float)
print("nausees_filecsv",nausees_filecsv )
fatigue_filecsv = from_csv_to_tuple(fatigue_file,float)
print("fatigue_filecsv",fatigue_filecsv)
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
# link all comparte object in hearchy
caracteristique_vacc.add_children([type_s,efficacite])
# print("carr", caracteristique_vacc)
posologie.add_children([nbr_dose,age,delais,temp_eff])
# print("pos", posologie)
cout.add_children([conservation,prix])
# print("cout", cout)
effait_sec.add_children([sapi,dapi,cephalees,hyperthermie,nausees,fatigue])
# print("eff", effait_sec)
criteria.add_children([caracteristique_vacc,posologie,cout,effait_sec])
# print("cr", criteria)
# raport = criteria.report(show=True)


print("final criteria \n", criteria.target_weights)    