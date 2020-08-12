from tools.helper_functions import get_descriptor

"""
The following properties are listed in each gaussian output file
without needing any additional math:

Bond Lengths
Bond Ngles
Mulliken Charges
APT Charges

"""

def get_A_P_bond_lengths(filename,atomids,phosid):
    """
    atom id's is the array of strings containing the gaussian atom ID (find using helper_function
        get_phosphine_carbon_numbers)
    Assumes that phosphorus is the first atom
    :return: arrray of float bond lengths in Angstroms of the central P to 
        surrounding Atom
    """
    return [get_descriptor(filename,
                r' ! R.*R\({},{}\)\s*?(.\.....).*?'.format(phosid,atomids[0]),
                "P-A{} bond length".format(atomids[0])),
            get_descriptor(filename,
                r' ! R.*R\({},{}\)\s*?(.\.....).*?'.format(phosid,atomids[1]),
                "P-A{} bond length".format(atomids[1])),
            get_descriptor(filename,
                r' ! R.*R\({},{}\)\s*?(.\.....).*?'.format(phosid,atomids[2]),
                "P-A{} bond length".format(atomids[2]))]

def get_A_P_A_bond_angles(filename,atomids,phosid):
    """
    
    """
    return [get_descriptor(filename, # A1 P A2
                r' ! A.*A\({},{},{}\)\s*?(.?..\.....).*?'.format(atomids[0],phosid,atomids[1]),
                "A{}-P-A{} bond length".format(atomids[0],atomids[1])),
            get_descriptor(filename, # A1 P A3
                r' ! A.*A\({},{},{}\)\s*?(.?..\.....).*?'.format(atomids[0],phosid,atomids[2]),
                "A{}-P-A{} bond length".format(atomids[0],atomids[2])),
            get_descriptor(filename, # A2 P A3
                r' ! A.*A\({},{},{}\)\s*?(.?..\.....).*?'.format(atomids[1],phosid,atomids[2]),
                "A{}-P-A{} bond length".format(atomids[1],atomids[2]))]

def get_mulliken_charges(filename,atomids,phosid):
    """
    Be sure to truncate file before entry, as desired mulliken charges are listed first AFTER optimization
    """
    #print(r'\s*?{}\s*?C\s*?(.?.\.......)\s*?'.format(atomids[2]))
    return [get_descriptor(filename, # P
                r'    {}  P\s*?(.?.\.......)\n'.format(phosid),
                "P{} mulliken charge".format(phosid)),
            get_descriptor(filename, # A1
                r'\s*?{}  [A-Z][a-z]?\s*?(.?.\.......)\n'.format(atomids[0]),
                "A{} mulliken charge".format(atomids[0])),
            get_descriptor(filename, #A2
                r'\s*?{}  [A-Z][a-z]?\s*?(.?.\.......)\n'.format(atomids[1]),
                "A{} mulliken charge".format(atomids[1])),
            get_descriptor(filename, # A3
                r'\s*?{}  [A-Z][a-z]?\s*?(.?.\.......)\n'.format(atomids[2]),
               "A{} mulliken charge".format(atomids[2]))]


def get_APT_charges(filename,atomids,phosid):
    """
    Be sure to truncate file with both truncate functions before entry, 
    as desired APT charges are listed first AFTER optimization
    """
    return [get_descriptor(filename, # P
                r'    {}  P\s*?(.?.\.......)\n'.format(phosid),
                "P{} APT charge".format(phosid)),
            get_descriptor(filename, # A1
                r'\s*?{}  [A-Z][a-z]?\s*?(.?.\.......)\n'.format(atomids[0]),
                "C{} APT charge".format(atomids[0])),
            get_descriptor(filename, # A2
                r'\s*?{}  [A-Z][a-z]?\s*?(.?.\.......)\n'.format(atomids[1]),
                "C{} APT charge".format(atomids[1])),
            get_descriptor(filename, # A3
                r'\s*?{}  [A-Z][a-z]?\s*?(.?.\.......)\n'.format(atomids[2]),
               "C{} APT charge".format(atomids[2]))]
