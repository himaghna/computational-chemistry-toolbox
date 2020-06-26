"""
@uthor: Himaghna, 25th November 2019
Description: Make Gaussian input files

"""
from os import mkdir, getcwd
import os.path
from argparse import ArgumentParser
import ase.io
from ase.calculators.gaussian import Gaussian
import glob


# use this to fine tune submission keywords for Gaussian
def format_root(header_flag, file_name, functional='m062x',
                basis='6-311g(2df,p)'):
     # create temp file in current working directory
    temp_file = os.path.join(os.getcwd(), 'temp') 

    with open(file_name, "r") as fp:
        lines = fp.readlines()

    with open(temp_file, "w") as fp:
        for line in lines:
            if header_flag in line:
                    # if line is header
                paste_line = f'# opt freq {basis} {functional} \n'
            else:
                paste_line = line
            fp.write(paste_line)

    os.remove(file_name) 
    # rename modified temp file to original filename
    os.rename(src=temp_file, dst=file_name)  


def write_gaussian(ase_object, out_dir, **kwargs):
    """
    Write a Gaussian input file based on an ase object.
    Params :: 
    ase_object: ASE IO Object: ASE file containing molecule used as input for 
        Gaussian input file
    out_dir: str: path of directory to write the Gaussian input file
    **kwargs: dict: additional arguments to modify behaviour of gaussian input

    Returns ::
    None

    """
     # this is used to identify the header line and replace it
    HEADER_FLAG = 'HEADER_FLAG'
    # change directory to destination where input file to be saved
    original_dir = getcwd()
    os.chdir(out_dir)
    gaussian_settings = {'method': HEADER_FLAG,
                            'basis': '6-31g',
                            'Opt': 'Tight',
                            'Freq': 'DiagFull ',
                            'multiplicity': 1,
                            'charge': 0,
                            'mem': '50GB',
                            'nproc': 20  # ***20 for Farber and 36 for Caviness 
                            }
    gaussian_settings.update(kwargs)
    # input file created will be gaussian_input.com
    calc = Gaussian(**gaussian_settings, label='gaussian_input')
    ase_object.set_calculator(calc)  
    calc.write_input(ase_object)
    # change back directories
    os.chdir(original_dir)
    format_root(header_flag=HEADER_FLAG,
                    file_name=os.path.join(out_dir, 'gaussian_input.com'))
    

def main():
    parser = ArgumentParser()
    parser.add_argument('-id', '--input_dir', required=True, \
        help='Input directory contains all the .xyz files')
    parser.add_argument('-od', '--output_dir', required=True, \
        help='Output directory contains all molecules and jobs as sub-folders')
    args = parser.parse_args()
    input_dir = args.input_dir
    output_dir = args.output_dir
    if not os.path.isdir(output_dir):
        print(f'Creating Output Directory at {output_dir}')
        mkdir(output_dir)
    # create jobfolders and put jobs in them
    job_count = 0
    for fpath in (glob.glob(os.path.join(input_dir, '*.xyz')):
        fname = os.path.basename(fpath).replace('.xyz', '') # only fname no ext
        new_folderpath = os.path.join(output_dir, fname)
        try:
            ase_object = ase.io.read(fpath)
        except:
            print(f'Could not create {fname}')
            continue
        if os.path.isdir(new_folderpath):
            print(f'{new_folderpath} ALREADY EXISTS!')
        else:
            mkdir(new_folderpath)
        # make job 
        print(f'Writing {fname}')
        write_gaussian(ase_object, new_folderpath)
        job_count += 1


if __name__ == "__main__":
    main()