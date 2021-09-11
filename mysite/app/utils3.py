import itertools
from ahpy import ahpy
def ahp_final():
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
    ('Delais', 'Temps_d_effet'): 1/2}
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
    print(keys)
    print(values)


ahp_final()


# ['Moderna', 'AstraZeneca', 'Sinovac', 'Janssen', 'Pfizer', 'sputnik']
# [0.279, 0.208, 0.153, 0.138, 0.122, 0.099]