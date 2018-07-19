Two tests are implemented here: 

1. A test of whether the ensemble is correct, and
2. A test of equipartition

To run these tests, first install the `physical_validation` module by calling `pip install physical_validation`. (Note that a bug in a package `physical_validation` is depending on might require you to first install `pip install numpy scipy matplotlib` before installing `pip install physical_validation`.) `physical_validation` works under python>=3.3 as well as python2.7. Note, however, that python2.7 is deprecated, and its support might be dropped in a future release. We strongly encourage you to use python>=3.3. To run the `ana_gromacs.py` ensemble check and the `ana.py` equipartition test, GROMACS should be installed, with the files changed to include the proper location of the GROMACS binary to be tested. 

Full documentation:
-------------------
Please see https://physical-validation.readthedocs.io for the full documentation of the validation package.

Directory structure:
--------------------

	ensemble/
		water/
			ana_gromacs.py
			ana_flatfile.py
			ana_pyarray.py
			top/
			md_NVT_be_1/
			md_NVT_vr_1/
			md_NVT_be_2/
			md_NVT_vr_2/

			md_NPT_be_1/
			md_NPT_vr_1/
			md_NPT_be_2/
			md_NPT_vr_2/
			md_NPT_be_3/
			md_NPT_vr_3/
			md_NPT_be_4/
			md_NPT_vr_4/

`python ana.py` performs the ensemble checks on a system of 900 water molecules. The `md_*` folders contain results of GROMACS simulations ran in different ensembles (NVT, NPT), using different thermostats ('vr' stands for velocity-rescale, 'be' for Berendsen thermostat), and at different state points (NVT: 1: T, 2: T+dT; NPT: 1: (T, P), 2: (T+dT, P), 3: (T, P+dP), 4: (T+dT, P+dP)). The `top/` folder contains the topology of the system.

`python ana_flatfile.py` performs the same NVT ensemble checks on the velocity rescale data set, with the data loaded from an ASCII files with a list of energies.

`python ana_numpy.py` performs the same NVT ensemble checks on the velocity rescale data set, with the data loaded from a numpy array of energies.
 
	equipartition/
		trp-cage/
			ana.py
			be_1/
			be_2/
			vr_1/
			vr_2/

`python ana.py` performs the equipartition check on a Trp-cage protein. The `be_*` and `vr_*` folders contain results of simulations ran in NPT using different thermostatting schemes: 'vr' stands for velocity-rescale, 'be' for Berendsen thermostat, while '_1' denotes a simulation using a single thermostat for the entire system, and '_2' denotes a simulation using two separate thermostats, one for the protein and one for the solvent. Note that the solvent was stripped from the trajectory files to considerably reduce file size and execution time for the workshop, so only the solute kinetic energy is analyzed.  `tot` is the total kinetic energy, `tra` is translational kinetic energy of the group, `rni` is the rotational plus internal, `rot` is the rotational kinetic energy, and `int` is the interna kinetic energy.

Some output notation used by the validation tools:
--------------------------------------------------
* Before analyzing the distributions, the trajectories are analyzed to obtain uncorrelated samples and remove unequilibrated data. This consists of three steps:
  1. Equilibration: Any data points at the beginning of the trajectory which are not yet equilibrated (simulation has reached steady state) are ignored.
  2. Decorrelation: After equilibration, the remaining data points are analyzed for correlations in time. If samples are found to be correlated, only a decorrelated subset is used.
  3. Tail pruning (optional): To avoid numerical noise to strongly influence the fitting of small data sets, the extreme values of the simulation might be discarded.
  The result of this procedure is reported as `After equilibration, decorrelation and tail pruning, XX% (YYY frames) of original trajectory remain.`

