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
    Assumes that phosphorus is the first atom
    :return: arrray of float bond lengths in Angstroms of the central P to 
        surrounding C
    """
    return [get_descriptor(filename,
                r' ! R1    R\(1,{}\)\s*?(.\.....).*?'.format(Catomids[0]),
                "P-C{} bond length".format(Catomids[0])),
            get_descriptor(filename,
                r' ! R2    R\(1,{}\)\s*?(.\.....).*?'.format(Catomids[1]),
                "P-C{} bond length".format(Catomids[1])),
            get_descriptor(filename,
                r' ! R3    R\(1,{}\)\s*?(.\.....).*?'.format(Catomids[2]),
                "P-C{} bond length".format(Catomids[2]))]

def get_C_P_C_bond_angles(filename,Catomids):
    """
    
    """
    return [get_descriptor(filename, # C1 P C2
                r' ! A1    A\({},1,{}\)\s*?(.?..\.....).*?'.format(Catomids[0],Catomids[1]),
                "C{}-P-C{} bond length".format(Catomids[0],Catomids[1])),
            get_descriptor(filename, # C1 P C3
                r' ! A2    A\({},1,{}\)\s*?(.?..\.....).*?'.format(Catomids[0],Catomids[2]),
                "C{}-P-C{} bond length".format(Catomids[0],Catomids[2])),
            get_descriptor(filename, # C2 P C3
                r' ! A3    A\({},1,{}\)\s*?(.?..\.....).*?'.format(Catomids[1],Catomids[2]),
                "C{}-P-C{} bond length".format(Catomids[1],Catomids[2]))]

def get_mulliken_charges(filename,Catomids):
    """
    Be sure to truncate file before entry, as desired mulliken charges are listed first AFTER optimization
    """
    #print(r'\s*?{}\s*?C\s*?(.?.\.......)\s*?'.format(Catomids[2]))
    return [get_descriptor(filename, # P
                r'    1  P\s*?(.?.\.......)\n',
                "P1 mulliken charge"),
            get_descriptor(filename, # C1
                r'\s*?{}  C\s*?(.?.\.......)\n'.format(Catomids[0]),
                "C{} mulliken charge".format(Catomids[0])),
            get_descriptor(filename, #C2
                r'\s*?{}  C\s*?(.?.\.......)\n'.format(Catomids[1]),
                "C{} mulliken charge".format(Catomids[1])),
            get_descriptor(filename, # C3
                r'\s*?{}  C\s*?(.?.\.......)\n'.format(Catomids[2]),
               "C{} mulliken charge".format(Catomids[2]))]
