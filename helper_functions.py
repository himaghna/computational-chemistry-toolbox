
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
    print(name+"not found!")
    return False