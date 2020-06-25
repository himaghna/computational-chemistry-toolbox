"""Read a collection of Gaussian .log files to get electronic energies and
   other thermochemistry
    Date: 10th December 2019
    
    
    Sample usecase
    --------------

    def sample():
        parser = ArgumentParser()
        parser.add_argument('super_dir', help='Superdirector containing all \
            the Jobfolders')
        args = parser.parse_args()
        super_dir = args.super_dir
        if not os.path.isdir(super_dir):
            raise FileNotFoundError(f'{super_dir} is not a valid folder')
        for sub_dir in IterateSubdirectories(super_dir):
            gaussian_fname = os.path.join(sub_dir, 'gaussian_input.log')
            elec_zep = get_electronic_zpe(gaussian_fname)
"""


import os.path
from argparse import ArgumentParser
import re

# from helper_files import IterateSubdirectories

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

def get_zpe(filepath):
    """
    :return: float zero point correction (Hartrees/atom) if found. 
        False if nothing found
    """
    return get_descriptor(filepath,
        r'Zero-point correction=[ ]*(-?\d+\.?\d+)',
        "Zero point correction")


def get_electronic_zpe(filepath):
    """
    :return: float elec_zpe (Hartrees/atom) if found. 
        False if nothing found
    """
    return get_descriptor(filepath,
        r'Sum of electronic and zero-point Energies=[ ]*(-?\d+\.?\d+)',
        "electronic energy")


def get_free_energy(filepath):
    """
    :return: float free energy in Hartree/ atom if found.
       Prints ('No free energy found') and returns False if none found.

    """
    return get_descriptor(filepath,
        r'Sum of electronic and thermal Free Energies=[ ]*(-?\d+\.?\d+)',
        "free energy")


def get_enthalpy(filepath):
    """
    :return: float Enthalpy in Hartree/ atom if found.
        Prints ('No enthalpy found') and returns False if none found.

    """
    return get_descriptor(filepath,
        r'Sum of electronic and thermal Enthalpies=[ ]*(-?\d+\.?\d+)',
        "enthalpy")

# 'D:\Research\Error_DFT\Data_fusion\Jobs' -qf 'D:\Research\Error_DFT\Data_fusion\QM9\xyz_choose_2000_for_gaussian'