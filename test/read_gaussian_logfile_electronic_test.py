import sys
sys.path.append("..")
import tools.read_gaussian_logfile_electronic as R
path = 'example_output.log'

assert R.get_free_energy(path) == -891.50911

assert R.get_enthalpy(path) == -891.446309

assert R.get_zpe(path) == 0.405718

assert R.get_electronic_zpe(path) == -891.465504

print("passed")
