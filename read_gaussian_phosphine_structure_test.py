from read_gaussian_phosphine_structure import *
from helper_functions import get_phosphine_carbon_numbers, truncate_pre_optimized

path = r'example_output.log'
truncate_pre_optimized(path)
path = r'example_output_truncated.log'
assert get_phosphine_carbon_numbers(path) == ['2','15','28']

assert get_C_P_bond_lengths(path,['2','15','28']) == [1.9391, 1.9592, 1.9165]