# import csv
# import sys
# import time

# import pandas  as pd
# import numpy as np
# import numpy
# file = "/home/ali/Documents/MasterIIproect/mysite/app/file.csv"
# fil = "/home/ali/Documents/MasterIIproect/MP.csv"
# # Matrix = np.array(list(csv.reader(open(file, "r"), delimiter=",")))
# Matrix = np.loadtxt(fil,dtype = str, skiprows=0, delimiter=',')
# matrix = np.array(list(csv.reader(open(file, "r"), delimiter=",")))
# # ages = np.genfromtxt(fil, delimiter=',')
# pandos = pd.read_csv(fil)

# print(Matrix)
# print("********")
# print(matrix)
# print("ùùùùùùù")
# print(pandos)
# arry = np.array(pandos)
# labels = matrix[0,1:]
# print('labels \n',labels)
# Alternatives = matrix[2:,0]
# print('Names \n',Alternatives)
# print("tupe",type(Alternatives))
# #Convert to string 
# out_array = numpy.array_str(Alternatives)
# print('Numpy array to strings: ',out_array)
# #Prints the array with type 
# print(type(out_array))
# list_n = list(out_array)
# print(list_n)
# hh = Alternatives.tolist()
# print("hh",hh)
# print(type(hh))
# print(type(hh[0]))
# s= []
# z = 1
# for i in hh:
#     print("###")
#     print(i)
#     s.append(z)
#     z +=1

#     print("***")
# print(s)    

print("*********************")
