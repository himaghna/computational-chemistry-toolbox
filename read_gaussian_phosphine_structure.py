from helper_functions import get_descriptor

"""
The following properties are listed in each gaussian output file
without needing any additional math:

Bond Lengths
Bond Ngles
Mulliken Charges
APT Charges

"""

def get_C_P_bond_lengths(filename,Catomids):
    """
    Catom id's is the array of strings containing the gaussian atom ID (find using helper_function
        get_phosphine_carbon_numbers)
    :return: arrray of float bond lengths in Angstroms of the central P to 
        surrounding C
    """
    return [get_descriptor(filename,
            r' ! R1    R\(1,{}\)\s*?(.\.....).*?'.format(Catomids[0]),
            "P-C bond lengths"),
            get_descriptor(filename,
            r' ! R2    R\(1,{}\)\s*?(.\.....).*?'.format(Catomids[1]),
            "P-C bond lengths"),
            get_descriptor(filename,
            r' ! R3    R\(1,{}\)\s*?(.\.....).*?'.format(Catomids[2]),
            "P-C bond lengths")]