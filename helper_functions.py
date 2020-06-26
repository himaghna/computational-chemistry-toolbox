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
            return float(m[1])
    print(name+" not found!")
    return False

def get_phosphine_carbon_numbers(filename):
    return [str(int(get_descriptor(filename, # carbon 1
        r' ! R1    R\(1,(.*)\).*?',
        "carbon 1 id number"))),
        str(int(get_descriptor(filename, # carbon 2
        r' ! R2    R\(1,(.*)\).*?',
        "carbon 2 id number"))),
        str(int(get_descriptor(filename, # carbon 3
        r' ! R3    R\(1,(.*)\).*?',
        "carbon 3 id number")))]

def truncate_pre_optimized(filename):
    """
    trims part of file which includes pre-optimized values
    """
    with open(filename) as file:
        filedata = file.readlines()
    pattern = re.compile(r'Optimization complete.')
    idx = 0
    begin = 0
    for line in filedata:
        m = pattern.search(line)
        if m:
            begin = idx
        else:
            idx = idx + 1
    with open(filename.replace(".log","") + "_truncated.log",'w') as file:
        file.writelines(filedata[(begin+1):])