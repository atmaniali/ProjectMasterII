import itertools

from ahpy import ahpy
import csv
import numpy as np

file = "vaccination.csv"

"""  """
matrice = np.array(list(csv.reader(open(file, "r"), delimiter=",")))
print(matrice)

"""  """