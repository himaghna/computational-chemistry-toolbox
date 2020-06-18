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

from helper_files import IterateSubdirectories


def get_zpe(filepath):
    """

    :param filepath: log file path
    :return: float zero point correction (Hartrees/atom) if found. 
        False if nothing found
    """
    with open(filepath, "r") as fp:
        file_data = fp.readlines()
    zpe_pattern = re.compile(r'Zero-point correction=[ ]*(-?\d+\.?\d+)')
    for line in file_data:
        m = zpe_pattern.search(line)
        if m:
            # match found
            zpe = m[1]
            return float(zpe)
    print('zero-point correction not found')
    return False


def get_electronic_zpe(filepath):
    """

    :param filepath: log file path
    :return: float elec_zpe (Hartrees/atom) if found. False if nothing found
    """
    with open(filepath, "r") as fp:
        file_data = fp.readlines()
    elec_zpe_pattern = re.compile(
        r'Sum of electronic and zero-point Energies=[ ]*(-?\d+\.?\d+)')
    for line in file_data:
        m = elec_zpe_pattern.search(line)
        if m:
            # pattern matches
            elec_zpe = m[1]
            return float(elec_zpe)
    print('no electronic energy found')
    return False


def get_free_energy(filepath):
    """Get the thermal free energy from a Gaussian logfile.

    Parameters
    ----------
    filepath : str
        Complete path of the Gaussian logfile.

    Returns
    -------
    float
       free energy in Hartree/ atom if found.
       Prints ('No free energy found') and returns False if none found.

    """
    with open(filepath, "r") as fp:
        file_data = fp.readlines()
    free_energy_pattern = re.compile(
        r'Sum of electronic and thermal Free Energies=[ ]*(-?\d+\.?\d+)')
    for line in file_data:
        m = free_energy_pattern.search(line)
        if m:
            # pattern matches
            free_energy = m[1]
            return float(free_energy)
    print('no free energy found')
    return False


def get_enthalpy(filepath):
    """Get the thermal enthalpy from a Gaussian logfile.

    Parameters
    ----------
    filepath : str
        Complete path of the Gaussian logfile.

    Returns
    -------
    float
       Enthalpy in Hartree/ atom if found.
       Prints ('No enthalpy found') and returns False if none found.

    """
    with open(filepath, "r") as fp:
        file_data = fp.readlines()
    enthalpy_pattern = re.compile(
        r'Sum of electronic and thermal Enthalpies=[ ]*(-?\d+\.?\d+)')
    for line in file_data:
        m = enthalpy_pattern.search(line)
        if m:
            # pattern matches
            enthalpy = m[1]
            return float(enthalpy)
    print('no enthalpy found')
    return False

# 'D:\Research\Error_DFT\Data_fusion\Jobs' -qf 'D:\Research\Error_DFT\Data_fusion\QM9\xyz_choose_2000_for_gaussian'