import itertools

from ahpy import ahpy
import csv
import numpy as np

critere = "criter.csv"
postologie = "sub_critere_postologie.csv"
effect_secondaire = "sub_critere_effect_secondaire.csv"
dictionnaire = {}
dictionnaire_p = {}
dictionnaire_es = {}

"""  """

matrice = np.array(list(csv.reader(open(critere, "r"), delimiter=",")))
matrice_postologie = np.array(list(csv.reader(open(postologie, "r"), delimiter=",")))
matrice_effet_secondaire = np.array(list(csv.reader(open(effect_secondaire, "r"), delimiter=",")))
print("matrice :\n")

print(matrice)
print(matrice_postologie)
print(matrice_effet_secondaire)

"""  """

line_matrice = matrice[0]
line_matrice_p = matrice_postologie[0]
line_matrice_es = matrice_effet_secondaire[0]

print("line matrice :\n")

print(line_matrice)
print(line_matrice_p)
print(line_matrice_es)

new_line_matrice = line_matrice[1:]
new_line_matrice_p = line_matrice_p[1:]
new_line_matrice_es = line_matrice_es[1:]

print("new line matrice :\n")

print(new_line_matrice)
print(new_line_matrice_p)
print(new_line_matrice_es)

"""  """

new_matrice = matrice[1:,1:]
new_matrice_p = matrice_postologie[1:,1:]
new_matrice_es = matrice_effet_secondaire[1:,1:]

new_matrice_float = new_matrice.astype(float)
new_matrice_p_float = new_matrice_p.astype(float)
new_matrice_es_float = new_matrice_es.astype(float)
print("new matrice :\n")
print(new_matrice)

"""  """

for i in range(len(new_matrice)):
    for j in range(len(new_matrice)):
        dictionnaire.update({(new_line_matrice[i],new_line_matrice[j]):new_matrice_float[i][j]}) 
print("dictionnaire :\n")

print(dictionnaire)

for i in range(len(new_matrice_p)):
    for j in range(len(new_matrice_p)):
        dictionnaire_p.update({(new_line_matrice[i],new_line_matrice_p[j]):new_matrice_p_float[i][j]}) 
print("dictionnaire :\n")

print(dictionnaire)

for i in range(len(new_matrice_es)):
    for j in range(len(new_matrice_es)):
        dictionnaire_es.update({(new_line_matrice_es[i],new_line_matrice_es[j]):new_matrice_es_float[i][j]}) 
print("dictionnaire :\n")

print(dictionnaire)
print(dictionnaire_p)
print(dictionnaire_es)

"""  """

criteria  = ahpy.Compare('Criteria', dictionnaire, precision=3)
report = criteria.report(show=True)

"""  """
vaccin = ('AstraZeneca', 'Sinovac', 'sputnik', 'Janssen', 'Pfizer', 'Moderna')
vaccin_pairs = list(itertools.combinations(vaccin, 2))
print("\n")
print("vaccin \n")
print(vaccin)
print("\n")
print("vaccin pairs \n")



print(vaccin_pairs)


