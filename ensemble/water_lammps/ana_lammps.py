# Full documentation at http://physical-validation.readthedocs.io/
import physical_validation as pv

# Create a LAMMPS parser
parser = pv.data.LammpsParser()

# In this example, we will only look at the simulations performed under
# NVT conditions using `fix nvt` (Nose-Hoover thermostat). There are two simulations:
# One ran at 300K, and one ran at 308K.
ensemble_1 = pv.data.EnsembleData(
    ensemble='NVT',
    natoms=100*3,
    volume=20**3,
    temperature=300
)
ensemble_2 = pv.data.EnsembleData(
    ensemble='NVT',
    natoms=100*3,
    volume=20**3,
    temperature=308
)
dir_1 = 'nh_1'
dir_2 = 'nh_2'

# We can now use the LAMMPS parser to create simulation results for the two NVT
# simulations, using the ensemble definitions created before:
result_1 = parser.get_simulation_data(
    ensemble=ensemble_1,
    in_file=dir_1 + '/water.in',
    log_file=dir_1 + '/log.lammps',
    data_file=dir_1 + '/water.lmp',
    dump_file=dir_1 + '/dump.atom'
)
result_2 = parser.get_simulation_data(
    ensemble=ensemble_2,
    in_file=dir_2 + '/water.in',
    log_file=dir_2 + '/log.lammps',
    data_file=dir_2 + '/water.lmp',
    dump_file=dir_2 + '/dump.atom'
)

# The LAMMPS parser is currently not able to set the number of constraints due
# to `fix shake` or `fix rattle` commands (see output of previous commands).
# We'll hence add this here (3 constraints per molecule):
result_1.system.nconstraints=300
result_2.system.nconstraints=300

# As with the other parsers, we can now test, for example, the kinetic energy using the
# created simulation result data structure, where
# the first input is the simulation results read in,
# `strict` determines whether we test the full distribution (True)
# or only determine the mean and the variance of the distribution (False),
# `verbosity` sets the level of detail of the output  (with verbosity=0
# being quiet and verbosity=3 being the most chatty), and the filename is being used to
# plot the resulting distribution for visual inspection.
print('==> Kinetic energy test of simulation ' + dir_1)
pv.kinetic_energy.distribution(result_1, strict=False, verbosity=2,
                               filename='ke_lammps_vr_NVT_1')
print('==> Kinetic energy test of simulation ' + dir_2)
pv.kinetic_energy.distribution(result_2, strict=False, verbosity=2,
                               filename='ke_lammps_vr_NVT_2')

# We can also test the distribution of the potential energy. While the first two
# inputs to the tests are the parsed simulation results, `verbosity` sets the level of
# detail of the output  (with verbosity=0 being quiet and verbosity=3 being the most chatty),
# and the filename is being used to plot the resulting distribution for visual inspection.
print('==> Potential energy test')
pv.ensemble.check(result_1, result_2,
                  verbosity=2, filename='pe_lammps_vr_NVT')
