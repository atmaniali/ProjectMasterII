# ahp.py

import numpy as np
from ahpy import ahpy
import csv

file = "test.csv"
file1 = "test1.csv"
dictionnaire = {}
matrice = []

class ahp:

# declaration of attrebute :
 
    def __init__(self,file, matrice, dictionnaire = {}):
        self.__file = file
        self.__dictionnaire = dictionnaire
        self.__matrice = matrice

# getteur of attrebute :

    def get_file(self):
        return self.__file 

    def get_dictionnaire(self):
        return self.__dictionnaire

    def get_matrice(self):
        return self.__matrice

# setteur of attrebute :

    def set_file(self, file):
        self.__file = file

    def set_dictionnaire(self, dictionnaire):
        self.__dictionnaire = dictionnaire

    def set_matrice(self,matrice ):
        self.__matrice = matrice                

# function for ahp :

    def csv_to_matrix(self, matrice):
        """ convert csv file to matrix return matrice"""
        # condition : file csv chould have floating number like xx.xx not x/x
        matrice = np.array(list(csv.reader(open(file, "r"), delimiter=",")))
        return matrice

    def extract_line_matrice(self, matrice):
        """  extract header of matrice  return table  """
        line_matrice = matrice[0]
        new_line_matrice = line_matrice[1:]
        return new_line_matrice 
    def new_matrice(self, matrice):  
        """ ? return matrice """
        new_matrice = matrice[1:,1:]
        # transfer matrice from char to float
        new_matrice_float = new_matrice.astype(float)
        return new_matrice_float

    def insert_in_dictionnaire(self, matrix,header_matrice):
        """ turn matrix into dictionnnaire return dictionnaire """
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                dictionnaire.update({(header_matrice[i],header_matrice[j]):matrix[i][j]})
        return dictionnaire 

# end class 


# executions :

ahp_execute = ahp(file,matrice)
matrice =ahp_execute.csv_to_matrix(matrice)
print(matrice) 
print(type(matrice))
line = ahp_execute.extract_line_matrice(matrice)
print(line)
new = ahp_execute.new_matrice(matrice)
dictionnaire= ahp_execute.insert_in_dictionnaire(new,line)
print(dictionnaire)
drinks = ahpy.Compare(name='Drinks', comparisons=dictionnaire, precision=3, random_index='saaty')
print("drinks.target_weights : %",drinks.target_weights)
print("drinks.consistency_ratio : ",drinks.consistency_ratio)
