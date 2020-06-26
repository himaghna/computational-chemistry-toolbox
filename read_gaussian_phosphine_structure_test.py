from read_gaussian_phosphine_structure import *
from helper_functions import get_phosphine_carbon_numbers, truncate_pre_optimized

#truncate pre-optimization so that parser does nto get caught up on initial setup
path = r'example_output.log'
truncate_pre_optimized(path)
path = r'example_output_truncated.log'

assert get_phosphine_carbon_numbers(path) == ['2','15','28']

assert get_C_P_bond_lengths(path,['2','15','28']) == [1.9391, 1.9592, 1.9165]

assert get_C_P_bond_lengths(r'blank.log',['2','15','28']) == [False, False, False]

assert get_C_P_C_bond_angles(path,['2','15','28']) == [109.8925, 104.4816, 100.6809]