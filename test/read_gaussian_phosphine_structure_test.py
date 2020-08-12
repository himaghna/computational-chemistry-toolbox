import sys
sys.path.append("..")
import tools.helper_functions as H
import tools.read_gaussian_phosphine_structure as R

#truncate pre-optimization so that parser does not get caught up on initial setup
path = r'example_output.log'
path = H.truncate_pre_optimized(path)

assert H.get_phosphine_phosphorus_number(path) == '1', H.get_phosphine_phosphorus_number(path)

phosid = H.get_phosphine_phosphorus_number(path)

assert H.get_phosphine_atom_numbers(path,phosid) == ['2','15','28'], H.get_phosphine_atom_numbers(path,phosid)

assert R.get_A_P_bond_lengths(path,['2','15','28'],phosid) == [1.9391, 1.9592, 1.9165], R.get_A_P_bond_lengths(path,['2','15','28'],phosid)

assert R.get_A_P_bond_lengths(r'blank.log',['2','15','28'],phosid) == [False, False, False], R.get_A_P_bond_lengths(r'blank.log',['2','15','28'],phosid) 

assert R.get_A_P_A_bond_angles(path,['2','15','28'],phosid) == [109.8925, 104.4816, 100.6809], R.get_A_P_A_bond_angles(path,['2','15','28'],phosid)

path = H.truncate_to_mulliken(path)

assert R.get_mulliken_charges(path,['2','15','28'],phosid) == [0.227783, -0.399331, -0.409120, -0.232924], print(R.get_mulliken_charges(path,['2','15','28'],phosid))

path = H.truncate_to_APT(path)

assert R.get_APT_charges(path,['2','15','28'],phosid) == [0.480742, -0.025829, 0.005156, -0.101836], print(R.get_APT_charges(path,['2','15','28'],phosid))

print("passed")
