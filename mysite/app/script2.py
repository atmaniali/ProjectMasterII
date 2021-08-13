# # import
import numpy as np
# import csv
# # turn file csv to matrix
# dictionnaire = {}
# Matrix = np.array(list(csv.reader(open("/home/ali/Documents/MasterIIproect/test.csv", "r"), delimiter=",")))
# print('Matrice ',Matrix)
# # exraire values from matrix
# matrix_list = Matrix[2:,1]
# print("hak",Matrix[2:,1])
# matrix = Matrix[2:,2:].astype(float)
# print("matrix \n ", matrix)
# # extrere first triangl of matrice and save in dictionnaire: \n
# for i in range(len(matrix_list)):
#     for j in range(len(matrix_list)):
#         if i < j:
#             dictionnaire.update({(matrix_list[i],matrix_list[j]):matrix[i][j]})
# print("dictionaire \n:", dictionnaire)   
# def convert_to_tuple(list):
#     return tuple(list)
         
# print("*", convert_to_tuple(matrix_list))           
def from_csv_to_dict(file):
    dictionnaire = {}
    Matrix = np.loadtxt(file,dtype = str, skiprows=0, delimiter=',')
    print(Matrix)
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
file = "/home/ali/Documents/MasterIIproect/ahp_csv_all/sub_critere_posologie.csv"
file_new = "/home/ali/Documents/MasterIIproect/ahp_csv_all/age.csv"
res = from_csv_to_dict(file)    
tup = from_csv_to_tuple(file_new, float)
print('res \n', res)
print('tup \n', tup)