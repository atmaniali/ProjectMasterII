from django.conf import settings
import numpy
import numpy as np
import pandas as pd
from django.core.files.storage import FileSystemStorage
import requests
import csv 
import random 




def get_all_provinces():
    provinces = requests.get('https://api.corona-dz.live/province/latest').json()
    data = []
    for province in provinces :
        data.append(province['data'])
   
    return provinces    


def convert_to_tuple(list):
    return tuple(list) 
# PROMETHEE_II
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
def changetozeros(matrix):
    for i in range(len(matrix)) :  
        for j in range(len(matrix[i])) :  
            if matrix[i][j] < 0 :
                matrix[i][j] = 0
    return matrix  
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
def add_aggregated_preferences_line(matrix):
    average_line_weight = []
    
    for i in range(len(matrix)) :
        sum = 0  
        for j in range(len(matrix[i])) :
            sum = sum + matrix[i][j] 
        average_line_weight.append(sum)
        
    matrix = np.vstack([matrix.transpose(), average_line_weight]).transpose()
    return matrix  
def create_aggregated_matrix(matrix, aggr):
    # retrieve only the aggregated column(list)
    aggregate_column = np.array(matrix[:, -1].transpose())
    agrs = aggr.tolist()
    print(aggregate_column)
    print("type of aggregate_column")
    print(type(aggregate_column))
    aggregated_matrix = [ [ 0 for i in range(len(matrix)) ] for j in range(len(matrix)) ]
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
           
def sumColumn(matrice):
    return [sum(col) for col in zip(*matrice)] 
def calculateflows(matrix):
    diffs=[]
    for i in range(len(matrix)):
        diffs.append(matrix[i,-1] - matrix[-1, i])
    return diffs
# TODO: Modify functions pls and elemate print
def readMatrix(MPfiles, weightfiles):
    
    Matrix = np.loadtxt(MPfiles,dtype = str, skiprows=0, delimiter=',')
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
    Preference_matrix = changetozeros(variables_possibilities)
    print('PREFERENCE_matrix \n', Preference_matrix)
    # time.sleep(3)
    # concatenate the Names and preferences related 
    the_Preference_matrix = np.hstack([Alternative_possibilities, Preference_matrix])
    print('the_Preference_matrix \n', the_Preference_matrix)
    # weights =list(csv.reader(open(weightfiles, "r"), delimiter=","))  
    # print('weights \n', weights)
    array_weights = np.loadtxt(weightfiles, delimiter=',', dtype=float)
    print('array_weights \n', array_weights)
    Agregate_preference_matrix = mult_matrix_vect(Preference_matrix, array_weights)
    show_calculation = show_mult_matrix_vect(Preference_matrix, array_weights)
    # lets add a column to sum these aggregated preferences
    Agregate_preference_matrix_with_sum = add_aggregated_preferences_line(Agregate_preference_matrix)
    print('Agregate_preference_matrix_with_sum \n', Agregate_preference_matrix_with_sum)
    # time.sleep(3)
    aggrsums = Agregate_preference_matrix_with_sum[:,-1]
    print(aggrsums)

    # take only the aggragated sum values(LAST column) and create aggregated preference Function(matrix)
    aggregated_matrix = np.zeros((len(Alternatives), len(Alternatives)))

    print("len alternatives")
    created_aggregated_matrix = create_aggregated_matrix(aggregated_matrix, aggrsums)

    print("HADA created_aggregated_matrix")
    print(created_aggregated_matrix)
    # time.sleep(3)
    duplicated = created_aggregated_matrix
    #flot entrant w sortant
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
    print("flowscreated_aggregated_matrix")
    differencesflots = calculateflows(created_aggregated_matrix)
    print("differencesflots /*")
    print(differencesflots)
    print("******************")


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
    print("flot net") 
    print(sortedArr[:,-1])
    type_tali = sortedArr[:,-1]
    listing = list(type_tali)
    risting = type_tali.tolist()
    print(listing)
    print(risting)
    print([float(x) for x in risting])
    final_float = [float(x) for x in risting]
    print("*************************************-******************************************")      
    final_sorted = sortedArr[:,0]
    # print("count finale :", len(final_sorted))
    # print("type{}".format(type(final_sorted)))
    # out_array = numpy.array_str(final_sorted)
    # list_np = []
    # for i in out_array:
    #     list_np.append(i)
    # print(list_np, 'list_np')    
    # print("type  list", type(list_np[0]))
    print("*****testing******")
    hh = final_sorted.tolist()
    # hh_1 = hh.remove(' ')
    # print("hh",hh_1)
    liza = []
    hay_3liya = []
    zero = 1
    for i in hh:
        if len(i) != 1:
            liza.append(i)
            hay_3liya.append(zero)
            zero = zero+1
    return liza , final_float 

doc_file = '/home/ali/Documents/MasterIIproect/proethee_csv/data2.csv'
weight_file = '/home/ali/Documents/MasterIIproect/proethee_csv/weight2.csv'
# promethe
result = readMatrix(doc_file, weight_file) 
  

def save_as_csv(query, name):
    list_np = np.array(query) 
    matrix = [ [ 0 for i in range(len(query)) ] for j in range(len(query)) ]
    for i in range(len(query)):
        for j in range(len(query)):
            if i == j:
                matrix[i][j] = 1
    matrix_np = np.array(matrix)  
    matrix_with_critere_ligne= np.vstack((list_np,matrix_np))
    matrix_transpose = matrix_with_critere_ligne.transpose()
    list_np = np.append("",list_np)
    matrix_with_critere_ligne_transpose= np.vstack((list_np,matrix_transpose))
    pd.DataFrame(matrix_with_critere_ligne_transpose).to_csv("media/files/critere_{}.csv".format(name))

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
def get_weight(liste):
    listes = []
    liste.remove(0.0)
    maxList = max(liste)
    z = [maxList + x for x in liste]
    sumes = sum(z)
    for x in z:
        listes.append((x*100)/sumes)
    return listes
# 1.1291917964816092
print("#### / ### / ")   
li =  [-0.007684481167234497, -0.09392203101888297, -0.12096867072395978, -0.25046135785523804, 0.0, 0.19073859164491294, 0.2822979491204023]
meth = get_weight(li)
print(meth)
"""create matrix from 2 vectors x for row and y for colomns"""
def get_matrix(x, y):
    x.insert(0,"")
    zeros = np.zeros((len(y),len(x)-1))
    mat = np.vstack([y,zeros.transpose()]).transpose()
    matrix = np.vstack([x,mat])
    return matrix

def get_matrix_ahp(x, y):
    zeros = np.zeros((len(y),len(x)))
    mat = np.vstack([y,zeros.transpose()]).transpose()
    x.insert(0,"")
    matrix = np.vstack([x,mat])
    return matrix

def get_list(x):
    zeros = np.zeros(len(x))
    matrix = np.vstack([x,zeros])
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
from app.models import Upload_csv, Upload_ahp
def numpy_to_csv(matrix, names,user,weights):
    matrix = np.array(matrix)
    urls = "media/promethee/{}_promethee_csv.csv".format(names)
    url = "promethee/{}_promethee_csv.csv".format(names)
    urls_weith = "media/promethee/{}_weight_csv.csv".format(names)
    url_weith = "promethee/{}_weight_csv.csv".format(names)
    rows = matrix[0,1:]
    colmns = matrix[1:,0]
    body=matrix[1:,1:]  
    df = pd.DataFrame(data=body, index=colmns, columns=rows)
    df.to_csv(urls)
    with open(urls_weith, 'w') as f:
       write = csv.writer(f)
       write.writerow(weights)
    mp_names = "mp_{}".format(names)
    weight_names = "weight_{}".format(names)
    a = Upload_csv.objects.create(user = user,
                                name = mp_names,
                                path = url,
                                weight_names = weight_names,
                                path_weight = url_weith) 
    print("a", a)          
""" turn weight to csv """     
# def weight_to_csv(weights, names, user):
#     urls_weith = "media/files/weight_csv{}.csv".format(names)
#     with open(urls_weith, 'w') as f:
#        write = csv.writer(f)
#        write.writerow(weights)  
#     Upload_csv.objects.create(user = user,name = names, path = urls)  
def numpy_to_csv_ahp(matrix, names, user):
    matrix = np.array(matrix)
    urls = "media/ahp/{}_ahp_csv.csv".format(names) 
    path = "ahp/{}_ahp_csv.csv".format(names)   
    rows = matrix[0,1:]
    colmns = matrix[1:,0]
    body=matrix[1:,1:]  
    df = pd.DataFrame(data=body, index=colmns, columns=rows)
    df.to_csv(urls)
    mp_names = "ahp_crit_{}".format(names)
    Upload_ahp.objects.create(
        user = user,
        name = mp_names,
        path = path
    )
import itertools
from ahpy import ahpy    
def ahp_finales():
    # //                                                                                                                           //
    critere_comparison = {('CarachterisiqueVaccin', 'Posologie'): 3, ('CarachterisiqueVaccin', 'Cout'): 5, ('CarachterisiqueVaccin', 'EffetsSecondaire'): 1,
    ('Posologie', 'Cout'): 3, ('Posologie', 'EffetsSecondaire'): 1/5,
    ('Cout', 'EffetsSecondaire'): 3}
    criteria = ahpy.Compare('Criteria', critere_comparison, precision=3)
    print()
    print('raport of criteria')
    print()
    report = criteria.report(show=True)
    # //                                                                                                                          //
    print()
    print('Subcriteria of CarachterisiqueVaccin ')
    print()
    caracterisiqueVaccin_comparison = {('Type', 'Efficacite'): 1/7}
    print()
    print('Subcriteria of Posologie')
    print()
    posologie_comparisons = {('NBrDose', 'Age'): 2, ('NBrDose', 'Delais'): 5, ('NBrDose', 'Temps_d_effet'): 1/3,
    ('Age', 'Delais'): 2, ('Age', 'Temps_d_effet'): 2,
    ('Delais', 'Temps_d_effet'): 1/2}
    print()
    print('Subcriteria of Cout ')
    print()
    cout_comparisons = {('Conservation', 'Prix'): 1/3}
    effets_secondaire_comparisons = {('sensibilité_au_point_injection','douleur_au_point_injection'):1,('sensibilité_au_point_injection','céphalées'):1/3,('sensibilité_au_point_injection','hyperthermie'):1/5,('sensibilité_au_point_injection','nausées'):1/3,('sensibilité_au_point_injection','fatigue'):3,
    ('douleur_au_point_injection','céphalées'):1/3,('douleur_au_point_injection','hyperthermie'):3,('douleur_au_point_injection','nausées'):1,('douleur_au_point_injection','fatigue'):1/3,
    ('céphalées','hyperthermie'):5,('céphalées','nausées'):1/3,('céphalées','fatigue'):1,
    ('hyperthermie','nausées'):1,('hyperthermie','fatigue'):1/5,
    ('nausées','fatigue'):3}
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
    type_values = (2, 1,1, 5, 5, 1/2, 1/2, 3, 3, 1, 5, 5, 5, 5, 1)
    type_comparisons = dict(zip(vaccin_pairs, type_values))
    print(type_comparisons)
    print()
    print('**************************************************************************************************** ')
    print()
    print("II")
    effecacite_values = (2, 1/5,1, 1/7, 1/4, 1/7, 1/3, 1/9, 1/7, 4, 1/2, 1, 1/8, 1/7, 2)
    effecacite_comparisons = dict(zip(vaccin_pairs, effecacite_values))
    print()
    print('**************************************************************************************************** ')
    print()
    print("III")
    nbr_dose_values = (1, 1, 1/2, 1, 1, 1, 1/2, 1, 1, 1/2, 1, 1, 2, 2, 1)
    nbr_dose_comparisons = dict(zip(vaccin_pairs, nbr_dose_values))
    print()
    print('**************************************************************************************************** ')
    print()
    print("IV")
    age_values = (1/4, 1/4, 1, 1/8, 1/8, 1, 4, 1/3, 1/3, 4, 1/3, 1/3, 1/8, 1/8, 1)
    age_comparisons = dict(zip(vaccin_pairs, age_values))
    print()
    print('**************************************************************************************************** ')
    print()
    print("V")
    delais_values = (1/7, 1/5, 1/9, 1/4, 1/4, 2, 1/2, 3, 3, 1/3, 2, 2, 4, 4, 1)
    delais_comparisons = dict(zip(vaccin_pairs, delais_values))
    print()
    print('**************************************************************************************************** ')
    print()
    print("VI")
    temps_effet_values = (1/3, 1/4, 1, 2, 1, 1/3, 3, 5, 3, 4, 6, 4, 2, 1, 1/2)
    temps_effet_comparisons = dict(zip(vaccin_pairs, temps_effet_values))
    print()
    print('**************************************************************************************************** ')
    print()
    print("VII")
    conservation_values = (1,1,1,4,2,1,1,4,2,1,4,2,4,2,1/2)
    conservation_comparisons = dict(zip(vaccin_pairs, conservation_values))
    print()
    print('**************************************************************************************************** ')
    print()
    print("VIII")
    prix_values = (4, 3, 2, 5, 5, 1/2, 1/3, 2, 2, 1/3, 3, 3, 4, 4, 1)
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
    sapi_values = (1/5, 1/5, 1/5, 1/5, 1/3, 1, 1,1 , 2, 1, 1, 2, 1, 2, 2)
    sapi_comparisons = dict(zip(vaccin_pairs, sapi_values))
    print('**************************************************************************************************** ')
    print()
    print("XI")
    dapi_values = (1/3, 1/4, 1/2, 2, 4, 1/2, 2, 4, 5, 4, 8, 9, 4, 5, 2)
    dapi_comparisons = dict(zip(vaccin_pairs, dapi_values))
    print()
    print('**************************************************************************************************** ')
    print()
    print("XII")
    cephalees_values = (1/4, 1/2, 1/3, 1, 2, 4, 4, 5, 7, 1/2, 2, 3, 3, 5, 2)
    cephalees_comparisons = dict(zip(vaccin_pairs, cephalees_values))
    print('**************************************************************************************************** ')
    print()
    print("XIII")
    hyperthermie_values = (1/5, 1/3, 1/4, 1/4, 1/3, 3, 2, 2, 3, 1/2, 1/2, 1, 1, 2, 2)
    hyperthermie_comparisons = dict(zip(vaccin_pairs, hyperthermie_values))
    print()
    print('**************************************************************************************************** ')
    print()
    print("XIV")
    nausées_values = (1/4, 1/4, 1/3, 2, 1, 1, 3, 5, 4, 3, 2, 4, 3, 2, 1/2)
    nausées_comparisons = dict(zip(vaccin_pairs, nausées_values))
    print('**************************************************************************************************** ')
    print()
    print("XV")
    fatigue_values = (1/4, 1/5, 1/3, 2, 3, 1/2, 3, 5, 6, 4, 6, 7, 3, 4, 2)
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
    return keys,values    