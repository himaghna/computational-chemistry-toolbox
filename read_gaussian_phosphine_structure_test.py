from read_gaussian_phosphine_structure import *
from helper_functions import *

#truncate pre-optimization so that parser does not get caught up on initial setup
path = r'example_output.log'
path = truncate_pre_optimized(path)

assert get_phosphine_phosphorus_number(path) == '1', get_phosphine_phosphorus_number(path)

phosid = get_phosphine_phosphorus_number(path)

assert get_phosphine_atom_numbers(path,phosid) == ['2','15','28'], get_phosphine_atom_numbers(path,phosid)

assert get_A_P_bond_lengths(path,['2','15','28'],phosid) == [1.9391, 1.9592, 1.9165], get_A_P_bond_lengths(path,['2','15','28'],phosid)

assert get_A_P_bond_lengths(r'blank.log',['2','15','28'],phosid) == [False, False, False], get_A_P_bond_lengths(r'blank.log',['2','15','28'],phosid) 

assert get_A_P_A_bond_angles(path,['2','15','28'],phosid) == [109.8925, 104.4816, 100.6809], get_A_P_A_bond_angles(path,['2','15','28'],phosid)

path = truncate_to_mulliken(path)

assert get_mulliken_charges(path,['2','15','28'],phosid) == [0.227783, -0.399331, -0.409120, -0.232924], print(get_mulliken_charges(path,['2','15','28'],phosid))

path = truncate_to_APT(path)

assert get_APT_charges(path,['2','15','28'],phosid) == [0.480742, -0.025829, 0.005156, -0.101836], print(get_APT_charges(path,['2','15','28'],phosid))