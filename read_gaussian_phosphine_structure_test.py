from read_gaussian_phosphine_structure import *
from helper_functions import *

#truncate pre-optimization so that parser does not get caught up on initial setup
path = r'example_output.log'
path = truncate_pre_optimized(path)

assert get_phosphine_carbon_numbers(path) == ['2','15','28'], get_phosphine_carbon_numbers(path)

assert get_C_P_bond_lengths(path,['2','15','28']) == [1.9391, 1.9592, 1.9165], get_C_P_bond_lengths(path,['2','15','28'])

assert get_C_P_bond_lengths(r'blank.log',['2','15','28']) == [False, False, False], get_C_P_bond_lengths(r'blank.log',['2','15','28']) 

assert get_C_P_C_bond_angles(path,['2','15','28']) == [109.8925, 104.4816, 100.6809], get_C_P_C_bond_angles(path,['2','15','28'])

path = truncate_to_mulliken(path)

assert get_mulliken_charges(path,['2','15','28']) == [0.227783, -0.399331, -0.409120, -0.232924], print(get_mulliken_charges(path,['2','15','28']))

path = truncate_to_APT(path)

assert get_APT_charges(path,['2','15','28']) == [0.480742, -0.025829, 0.005156, -0.101836], print(get_APT_charges(path,['2','15','28']))