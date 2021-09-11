import random 
import numpy as np  
import pandas as pd  
import numpy
import csv


# prometheeII
def csv_to_numpy_array(matrix,weights):
    Matrix = np.loadtxt(matrix,dtype = str, skiprows=0, delimiter=',')
    array_Matrix  = np.array(Matrix)
    array_weights = np.loadtxt(weights, delimiter=',', dtype=float)
    return array_Matrix, array_weights

def promethe_II(matrix,weights):
    Matrix, Weights = csv_to_numpy_array(matrix,weights)
    print(Matrix)
    Alternative_matix = Matrix[2:,1:].astype(np.single)
    print('Alternative_matix \n',Alternative_matix)
    labels = Matrix[0,1:]
    print('labels \n',labels)
    Alternatives = Matrix[2:,0]
    print('Names \n',Alternatives)
    maximisation = Matrix[1,1:]
    print('Beneficial or Not  \n',maximisation)

# Methodes or promethee
"""create matrix from 2 vectors x for row and y for colomns"""
def get_matrix(x, y):
    x.insert(0,"")
    zeros = np.zeros((len(y),len(x)-1))
    mat = np.vstack([y,zeros.transpose()]).transpose()
    matrix = np.vstack([x,mat])
    return matrix
 
""" add a list to matrix and return matrix for prometheeII"""   
def slicing(matrix):
    matrix = np.array(matrix)
    mat_header  = matrix[0]  
    mat_body = matrix[1:]  
    test = ['test']
    rend = random.choices(['yes','no'], k=len(mat_header)-1)
    test.extend(rend)
    # print(test)
    mat_header = np.vstack([mat_header,test])
    matrix = np.vstack([mat_header,mat_body])
    return matrix
""" turn numpy table into csv file"""
def numpy_to_csv(matrix):
    matrix = np.array(matrix)
    urls = "/home/ali/Documents/MasterIIproect/proethee_csv/data4.csv"
    rows = matrix[0,1:]
    colmns = matrix[1:,0]
    body=matrix[1:,1:]
    df = pd.DataFrame(data=body, index=colmns, columns=rows)
    df.to_csv(urls)  

""" turn weight to csv """     
def weight_to_csv(weights):
    urls = "/home/ali/Documents/MasterIIproect/proethee_csv/weights3.csv"
    with open(urls, 'w') as f:
       write = csv.writer(f)
       write.writerow(weights)  

# Variables
mat = "/home/ali/Documents/MasterIIproect/proethee_csv/data4.csv"
wei = "/home/ali/Documents/MasterIIproect/proethee_csv/weights3.csv"
mat1 = "/home/ali/Documents/MasterIIproect/proethee_csv/data2.csv"
wei1 = "/home/ali/Documents/MasterIIproect/proethee_csv/weight2.csv"
table = [
    ['', 'Foo', 'Bar', 'Barf'],
    ['Spam', 101, 102, 103],
    ['Eggs', 201, 202, 203],] 

# promethe_II(mat,wei)  #New csv  
# # promethe_II(mat1,wei1)  #Worck   
mat = slicing(table) 
print(mat)