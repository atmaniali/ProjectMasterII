# import
import numpy as np
import csv
# turn file csv to matrix
dictionnaire = {}
Matrix = np.array(list(csv.reader(open("mysite/media/files/data2.csv", "r"), delimiter=",")))
print('Matrice ',Matrix)
# exraire values from matrix
matrix_list = Matrix[2:,1]
print("hak",Matrix[2:,1])
matrix = Matrix[2:,2:].astype(float)
print("matrix \n ", matrix)
# extrere first triangl of matrice and save in dictionnaire: \n
for i in range(len(matrix_list)):
    for j in range(len(matrix_list)):
        if i < j:
            dictionnaire.update({(matrix_list[i],matrix_list[j]):matrix[i][j]})
print("dictionaire \n:", dictionnaire)   
def convert_to_tuple(list):
    return tuple(list)
         
print("*", convert_to_tuple(matrix_list))           