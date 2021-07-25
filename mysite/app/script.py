"""
this scripts for turn our models to numpy array then to csv_file for make user choice of
charge his values and start process of AHP methode 
"""
# *****************************************
# PHASE I : turn models into matrix and transfer into csv file
# import 
import numpy as np
import pandas as pd
import csv
# Stocker list
query = ["a","b","c","d","e"]
# Size of list
query_list = len(query)
# this for extrire date from models
# list_critere = []
# for i in query:
#     list_critere.append(i.name) 
# transfer our list into array list
list_np = np.array(query) 
hak = np.array(["a","b","c","d","e","f"])   
matrix = [ [ 0 for i in range(query_list) ] for j in range(query_list) ]

for i in range(len(query)):
    for j in range(len(query)):
        if i == j:
            matrix[i][j] = 1
matrix_np = np.array(matrix)  
print("matrix_np  \n",matrix_np)
print("matrix \n", matrix)
# add row to matrix 
matrix_with_critere_ligne= np.vstack((list_np,matrix_np))
print("matrix_critere ligne \n",matrix_with_critere_ligne)
# transpose matrix
matrix_transpose = matrix_with_critere_ligne.transpose()
print("transpose matrix : \n",matrix_transpose)
# add row to matrix 
list_np = np.append("",list_np)
matrix_with_critere_ligne_transpose= np.vstack((list_np,matrix_transpose))
print("matrix_critere ligne & new ligne \n",matrix_with_critere_ligne_transpose)
# turn into csv file
data = pd.DataFrame(matrix_with_critere_ligne_transpose).to_csv("mysite/media/files/data.csv")
print("df \n", data)
# NOTE: for subcritere they must have step in plus
# extraire all subcriteria hows have reations with criteria
# ******************************************
# STEP II : TAKE fichier AND TURN TO DICTIONNAIRE
Matrix = np.array(list(csv.reader(open("mysite/media/files/data2.csv", "r"), delimiter=",")))
print('Matrice ',Matrix)

