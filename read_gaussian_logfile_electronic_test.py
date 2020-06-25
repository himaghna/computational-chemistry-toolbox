from read_gaussian_logfile_electronic import *

path = r'example_output.log'

assert get_free_energy(path) == -853.447223

assert get_enthalpy(path) == -853.383101

assert get_zpe(path) == 0.394689

assert get_electronic_zpe(path) == -853.40311
