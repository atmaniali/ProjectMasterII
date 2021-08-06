import csv
import sys
import time

import numpy
import numpy as np
file = "/home/ali/Documents/MasterIIproect/mysite/app/file.csv"
fil = "/home/ali/Documents/MasterIIproect/MP.csv"
# Matrix = np.array(list(csv.reader(open(file, "r"), delimiter=",")))
Matrix = np.loadtxt(fil,dtype = str, skiprows=0, delimiter=',')

print(Matrix)
# Create the Alternatives Possibilities array[m1-m2,........]                       
def all_alternatives(Alternatives):
    Alternative_possibilities = []
    for i in range(len(Alternatives)):
        for j in range(len(Alternatives)):
            if i == j:
                pass
            else:
                Alternative_possibilities.append(Alternatives[i]+'-'+Alternatives[j])
    return np.array(Alternative_possibilities).reshape(len(Alternative_possibilities),1)
# create the matrix of all variables possibilities:
def all_variables(matrix):
    new_matrix = []
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if i == j:
                pass
            else:
                new_matrix.append(matrix[i]-matrix[j])
    return np.array(new_matrix)    
# STEP 1 : Normalize the Evaluation Matrix
array_Matrix  = np.array(Matrix)
Alternative_matix = array_Matrix[2:,1:].astype(np.single)
print('Alternative_matix \n',Alternative_matix)
labels = array_Matrix[0,1:]
print('labels \n',labels)
Alternatives = array_Matrix[2:,0]
print('Names \n',Alternatives)
maximisation = array_Matrix[1,1:]
print('Beneficial or Not  \n',maximisation)
# Get min and max for each criteria
min_criteria_array = Alternative_matix.min(axis=0)
print('min_criteria_array \n',min_criteria_array)
max_criteria_array = Alternative_matix.max(axis=0)
print('max_criteria_array \n',max_criteria_array)
for i in range(len(Alternative_matix)):
    for j in range(len(Alternative_matix[i])):
        if maximisation[j] == 'yes':
            Alternative_matix[i][j] = (max_criteria_array[j]-Alternative_matix[i][j])/(max_criteria_array[j]-min_criteria_array[j])
        else:
            Alternative_matix[i][j] = (Alternative_matix[i][j]-min_criteria_array[j])/(max_criteria_array[j]-min_criteria_array[j])
print('Alternative_matix \n',Alternative_matix)
# STEP 2 : Calculate Evaluative ieme per the othere {m1-m2 | m1-m3 | ....}
# Create the Alternatives Possibilities array[m1-m2,........]              
Alternative_possibilities = all_alternatives(Alternatives)
print('Alternative_possibilities \n', Alternative_possibilities)
# create the matrix of all variables possibilities:
variables_possibilities = all_variables(Alternative_matix)
print('variables_possibilities \n', variables_possibilities)
print('Alternative_possibilities shape \n', Alternative_possibilities.shape)
print('variables_possibilities shape \n', variables_possibilities.shape)
# concatenate the Names and variables related 
the_all_matrix = np.hstack([Alternative_possibilities, variables_possibilities])
print('The All Matrix \n', the_all_matrix)
# "STEP 3 : Calculate the PREFERENCE Function"
# Create an updated matrix that return 0 if value is negative or equal to 0 
# else keep value as it it
def changetozeros(matrix):
    for i in range(len(matrix)) :  
        for j in range(len(matrix[i])) :  
            if matrix[i][j] < 0 :
                matrix[i][j] = 0
    return matrix
Preference_matrix = changetozeros(variables_possibilities)
print('PREFERENCE_matrix \n', Preference_matrix)
time.sleep(3)
# concatenate the Names and preferences related 
the_Preference_matrix = np.hstack([Alternative_possibilities, Preference_matrix])
print('the_Preference_matrix \n', the_Preference_matrix)
weights =list(csv.reader(open("/home/ali/Documents/MasterIIproect/weight.csv", "r"), delimiter=","))  
print('weights \n', weights)
array_weights = np.asarray(weights[0], dtype='float')
print('array_weights \n', array_weights)
def mult_matrix_vect(matrix, weight):
    for i in range(len(matrix)) :  
        for j in range(len(matrix[i])) :  
            matrix[i][j] = matrix[i][j]* weight[j]
    return matrix
def show_mult_matrix_vect(matrix, weight):
    data = []
    for i in range(len(matrix)) :  
       
        for j in range(len(matrix[i])) : 
           
            data.append('{}*{}'.format(weight[j],matrix[i][j]))
    return np.array(data)

Agregate_preference_matrix = mult_matrix_vect(Preference_matrix, array_weights)
show_calculation = show_mult_matrix_vect(Preference_matrix, array_weights)
# lets add a column to sum these aggregated preferences
def add_aggregated_preferences_line(matrix):
    average_line_weight = []
    
    for i in range(len(matrix)) :
        sum = 0  
        for j in range(len(matrix[i])) :
            sum = sum + matrix[i][j] 
        average_line_weight.append(sum)
        
    matrix = np.vstack([matrix.transpose(), average_line_weight]).transpose()
    return matrix

Agregate_preference_matrix_with_sum = add_aggregated_preferences_line(Agregate_preference_matrix)
print('Agregate_preference_matrix_with_sum \n', Agregate_preference_matrix_with_sum)
time.sleep(3)
aggrsums = Agregate_preference_matrix_with_sum[:,-1]
print(aggrsums)

# take only the aggragated sum values(LAST column) and create aggregated preference Function(matrix)
def create_aggregated_matrix(matrix, aggr):
    # retrieve only the aggregated column(list)
    aggregate_column = np.array(matrix[:, -1].transpose())
    agrs = aggr.tolist()
    print(aggregate_column)
    print("type of aggregate_column")
    print(type(aggregate_column))
    for i in range(len(matrix)) :  
        print("***//****aggregated matrix*//**", len(aggregated_matrix))
        print("***//**len matrix**//**", len(matrix))
        for j in range(len(matrix[i])) :       
            if i == j:
                aggregated_matrix[i][j] = 0        
            else:  
                aggregated_matrix[i][j]= agrs[0]
                agrs.pop(0) 
            
                
                # aggregated_matrix.append(aggregate_column[j])
    # print('lol',aggregated_matrix)
    print(np.array(aggregated_matrix).shape)
    return aggregated_matrix
    
aggregated_matrix = np.zeros((len(Alternatives), len(Alternatives)))

print("len alternatives")
created_aggregated_matrix = create_aggregated_matrix(aggregated_matrix, aggrsums)

print("HADA created_aggregated_matrix")
print(created_aggregated_matrix)
time.sleep(3)
duplicated = created_aggregated_matrix
#flot entrant w sortant
def sumColumn(matrice):
    return [sum(col) for col in zip(*matrice)] 

sommeeecolonne= sumColumn(created_aggregated_matrix)

sumrows = np.sum(created_aggregated_matrix, axis = 1)
#we need to deivde those calculated values on the number of alternatives -1
newsommecolonne = []
newsumrow= []
for x in sommeeecolonne:
    newsommecolonne.append(x /(len(created_aggregated_matrix) - 1))

for x in sumrows:
    newsumrow.append(x /(len(created_aggregated_matrix) - 1))
   
print("flots entrants \n" , newsommecolonne)
print("flots sortants \n" , newsumrow)

created_aggregated_matrix = np.vstack([created_aggregated_matrix, newsumrow])
print("updated matrix with columns ")
print(created_aggregated_matrix)

newsommecolonne.append(0)
created_aggregated_matrix= np.vstack([created_aggregated_matrix.transpose(), newsommecolonne]).transpose()
print("created_aggregated_matrix kamel\n", created_aggregated_matrix)


#here i'll be using a function to calculate the flots 
def calculateflows(matrix):
    diffs=[]
    for i in range(len(matrix)):
        diffs.append(matrix[i,-1] - matrix[-1, i])
    return diffs

print("flowscreated_aggregated_matrix")
differencesflots = calculateflows(created_aggregated_matrix)
print(differencesflots)


alt = np.append(Alternatives, " ")
duplicated = np.vstack([alt, created_aggregated_matrix.transpose()])
#so far created_aggregated_matrix is transposed 


# def remove_last_element(arr):
#     return arr[np.arange(arr.size - 1)]
# fachnhat = remove_last_element(fachnhat)

talyabachtetsetef  = np.vstack([duplicated, differencesflots]).transpose()


print("##############")
with numpy.printoptions(threshold=numpy.inf):
    print(talyabachtetsetef[:-1,:])

# Sort 2D numpy array by first column
sortedArr = talyabachtetsetef[talyabachtetsetef[:,-1].argsort()]
print('Sorted 2D Numpy Array')
print("##############")
with numpy.printoptions(threshold=numpy.inf):
    print(np.flipud(sortedArr))
print("Final Sort is : ")
print(sortedArr[:,0])  
print("*************************************-******************************************")      
final_sorted = sortedArr[:,0]
print("count finale :", len(final_sorted))
print("type{}".format(type(final_sorted)))
out_array = numpy.array_str(final_sorted)
print(type(out_array[1]))
listin  = list(out_array)
print("list", listin)
list_np = []
for i in out_array:
    list_np.append(i)
print(list_np, 'list_np')    
print("type  list", type(list_np[0]))
print("*****testing******")
hh = final_sorted.tolist()
print("hh",hh)
print("hh",hh)
nekf = []
ss = 0
for i in hh:
    print(type(i))
    nekf.append(i)
    print("nek list \n", nekf[ss])
    ss +=1
np_p = np.array(nekf)
print(np_p) 
print("\n")
print("*********")   
str_np_p = numpy.array2string(np_p)
print(str_np_p)
print("\n")
# hh ['1326    ', '732     ', '729     ', '748     ', '737     ', '740     ', '1324    '
# , '1045    ', '743     ',
#  ' ', '1033    ', '1038    ', '1233    ',
#  '1321    ', '745     ', '1030    ', '1046    ', '1239    ', '1236    ']