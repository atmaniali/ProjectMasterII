import numpy as np
from ahpy import ahpy
import csv
import itertools

# 
criteria_comparisons = {('Cost', 'Safety'): 3, ('Cost', 'Style'): 7, ('Cost', 'Capacity'): 3,
    ('Safety', 'Style'): 9, ('Safety', 'Capacity'): 1,
    ('Style', 'Capacity'): 1/7}
criteria = ahpy.Compare('Criteria', criteria_comparisons, precision=3)
    # Show all of criteria report
report_creteria = criteria.report(show=True)
    # 
print("type of report creteria",type(report_creteria))
    # Subcreteria :
    # Coast comparison have 4 subcreteria  
cost_comparisons = {('Price', 'Fuel'): 2, ('Price', 'Maintenance'): 5, ('Price', 'Resale'): 3,
    ('Fuel', 'Maintenance'): 2, ('Fuel', 'Resale'): 2,
    ('Maintenance', 'Resale'): 1/2}
    #  Capacitycreia have 2 subcreteria
capacity_comparisons = {('Cargo', 'Passenger'): 1/5}
    # Alternative we have : 6
vehicles = ('Accord Sedan', 'Accord Hybrid', 'Pilot', 'CR-V', 'Element', 'Odyssey')
    # make theme en 2 pairs
vehicle_pairs = list(itertools.combinations(vehicles, 2))
print(vehicle_pairs)
    # we made relation alternative subcreteria
    # {Start}
price_values = (9, 9, 1, 1/2, 5, 1, 1/9, 1/9, 1/7, 1/9, 1/9, 1/7, 1/2, 5, 6)
price_comparisons = dict(zip(vehicle_pairs, price_values))
print(price_comparisons)
safety_values = (1, 5, 7, 9, 1/3, 5, 7, 9, 1/3, 2, 9, 1/8, 2, 1/8, 1/9)
safety_comparisons = dict(zip(vehicle_pairs, safety_values))

passenger_values = (1, 1/2, 1, 3, 1/2, 1/2, 1, 3, 1/2, 2, 6, 1, 3, 1/2, 1/6)
passenger_comparisons = dict(zip(vehicle_pairs, passenger_values))

fuel_values = (1/1.13, 1.41, 1.15, 1.24, 1.19, 1.59, 1.3, 1.4, 1.35, 1/1.23, 1/1.14, 1/1.18, 1.08, 1.04, 1/1.04)
fuel_comparisons = dict(zip(vehicle_pairs, fuel_values))

resale_values = (3, 4, 1/2, 2, 2, 2, 1/5, 1, 1, 1/6, 1/2, 1/2, 4, 4, 1)
resale_comparisons = dict(zip(vehicle_pairs, resale_values))

maintenance_values = (1.5, 4, 4, 4, 5, 4, 4, 4, 5, 1, 1.2, 1, 1, 3, 2)
maintenance_comparisons = dict(zip(vehicle_pairs, maintenance_values))

style_values = (1, 7, 5, 9, 6, 7, 5, 9, 6, 1/6, 3, 1/3, 7, 5, 1/5)
style_comparisons = dict(zip(vehicle_pairs, style_values))

cargo_values = (1, 1/2, 1/2, 1/2, 1/3, 1/2, 1/2, 1/2, 1/3, 1, 1, 1/2, 1, 1/2, 1/2)
cargo_comparisons = dict(zip(vehicle_pairs, cargo_values))
    # {End}
    # startcalcul
    # create corresponding Compare objects:
cost = ahpy.Compare('Cost', cost_comparisons, precision=3)
capacity = ahpy.Compare('Capacity', capacity_comparisons, precision=3)
price = ahpy.Compare('Price', price_comparisons, precision=3)
safety = ahpy.Compare('Safety', safety_comparisons, precision=3)
passenger = ahpy.Compare('Passenger', passenger_comparisons, precision=3)
fuel = ahpy.Compare('Fuel', fuel_comparisons, precision=3)
resale = ahpy.Compare('Resale', resale_comparisons, precision=3)
maintenance = ahpy.Compare('Maintenance', maintenance_comparisons, precision=3)
style = ahpy.Compare('Style', style_comparisons, precision=3)
cargo = ahpy.Compare('Cargo', cargo_comparisons, precision=3)
    # End calcul
    # The final step is to link all of the Compare objects into a hierarchy. First, 
    # we'll make the Price, Fuel, Maintenance and Resale objects the children of the Cost object...
cost.add_children([price, fuel, maintenance, resale])
capacity.add_children([cargo, passenger])
    # Now that the hierarchy represents the decision problem, 
    # we can print the target weights of the highest level Criteria object to see the results of the analysis:
criteria.add_children([cost, safety, style, capacity])
print(criteria.target_weights)