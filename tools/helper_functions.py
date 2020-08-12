import re

def get_descriptor(filepath,regex,name):
    """
    Helper function to build requests 

    :param filepath: path to logfile
    :param regex: Regular expression (as a raw string) used to locate the descriptor
    :param name: String containing name of parameters in case not found
    :return: float zero point descriptor if found. 
        False if nothing found
    """
    with open(filepath, "r") as file:
        file_data = file.readlines()
    pattern = re.compile(regex)
    for line in file_data:
        m = pattern.search(line)
        if m:
            # match found
            # print(line)
            # print(m)
            # print(m[1])
            # print(float(m[1]))
            return float(m[1])
    print(name+" not found!")
    return False

def get_phosphine_phosphorus_number(filename):
    """
    returns gaussian atom id for the phosphorus atom.

    Assumes that the central phoshine phosphorus is the only P in the molecule, or that it at least appears before any others.
    """
    return str(int(get_descriptor(filename,
        r'     (\d+)  P    .*?',
        # r'     (.*)  P.*?',
        "phosphorus id number")))

def get_phosphine_atom_numbers(filename, phosid):
    """
    returns array of gaussian atom ID's for the 3 atoms attached to phosphorus.
    """
    return [str(int(get_descriptor(filename, # atom 1
        r' ! R1    R\({},(\d+)\).*?'.format(phosid),
        "atom 1 id number"))),
        str(int(get_descriptor(filename, # atom 2
        r' ! R2    R\({},(\d+)\).*?'.format(phosid),
        "atom 2 id number"))),
        str(int(get_descriptor(filename, # atom 3
        r' ! R3    R\({},(\d+)\).*?'.format(phosid),
        "atom 3 id number")))]

def truncate_to(filename,regex,outfilename):
    with open(filename) as file:
        filedata = file.readlines()
    pattern = re.compile(regex)
    idx = 0
    begin = 0
    for line in filedata:
        m = pattern.search(line)
        if m:
            begin = idx
            break
        else:
            idx = idx + 1
    with open(filename.replace(".log","") + "_{}.log".format(outfilename),'w') as file:
        file.writelines(filedata[(begin+1):])
    return filename.replace(".log","") + "_{}.log".format(outfilename)

def truncate_pre_optimized(filename):
    """
    trims part of file which includes pre-optimized values
    """
    return truncate_to(filename,r'Optimization complete.',"opt")

def truncate_to_mulliken(filename):
    """
    trims part of file which includes pre-optimized values and location matrix
    """
    return truncate_to(filename,r'Mulliken charges:',"mul")

def truncate_to_APT(filename):
    """
    trims part of file which includes pre-optimized values and location matrix
    """
    return truncate_to(filename,r' APT charges:',"APT")