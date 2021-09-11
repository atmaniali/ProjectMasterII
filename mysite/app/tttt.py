from pprint import pprint

from ahpy import Compare

experience_comparisons = {
    ('Moll', 'Nell'): 1/4,
    ('Moll', 'Sue'): 4,
    ('Nell', 'Sue'): 9,
} 
education_comparisons = {
    ('Moll', 'Nell'): 3,
    ('Moll', 'Sue'): 1/5,
    ('Nell', 'Sue'): 1/7,
} 
charisma_comparisons = {
    ('Moll', 'Nell'): 5,
    ('Moll', 'Sue'): 9 ,
    ('Nell', 'Sue'): 4,
} 
age_comparisons = {
    ('Moll', 'Nell'): 1/3,
    ('Moll', 'Sue'): 5,
    ('Nell', 'Sue'): 9,
}
criteria_comparisons = {
    ('Experience', 'Education'): 4,
    ('Experience', 'Charisma'): 3,
    ('Experience', 'Age'): 7, 
    ('Education', 'Charisma'): 1/3,
    ('Education', 'Age'): 3,
    ('Charisma', 'Age'): 5,
}

experience = Compare('Experience', experience_comparisons, precision=3, random_index='saaty')
education = Compare('Education', education_comparisons, precision=3, random_index='saaty')
charisma = Compare('Charisma', charisma_comparisons, precision=3, random_index='saaty')
age = Compare('Age', age_comparisons, precision=3, random_index='saaty')
criteria = Compare('Criteria', criteria_comparisons, precision=3, random_index='saaty')

criteria.add_children([experience, education, charisma, age])

#pprint(criteria.target_weights)

#pprint(experience.local_weights)
#consistency_experience = True if experience.consistency_ratio < 10 else False
#print(experience.consistency_ratio, consistency_experience, experience.weight)

#pprint(education.global_weights)
#consistency_education= True if experience.consistency_ratio < 10 else False
#print(education.consistency_ratio, consistency_education,education.weight)

report = criteria.report(show=True)
print("********************** ********** *** * *")    
print("\n")
rep = experience.report(show=True)