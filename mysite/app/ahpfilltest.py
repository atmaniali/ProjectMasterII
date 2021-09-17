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

critere_file = "/home/ali/Documents/MasterIIproect/ahp_csv_all/criter.csv"
critere_filecsv = from_csv_to_dict(critere_file)
print(critere_filecsv)
critere_comparison = critere_filecsv
criteria = ahpy.Compare('Criteria', critere_comparison, precision=3)
a = criteria.target_weights
print("criteria \n",a) 
print(type(a))
keys = a.keys()
values = a.values()
values = list(values)
keys = list(keys)
print(keys)
values = []
# for keys valuesin a.i:
#     keys   