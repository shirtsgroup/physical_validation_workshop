#full documentation at http://physical-validation.readthedocs.io/
import physical_validation as pv

#MRS: I put in the default installs instead
# gromacs parser
gmx = pv.data.GromacsParser(exe='gmx',
                            includepath='/usr/local/share/gromacs/top/')

dirs = ['vr_1', 'vr_2', 'be_1', 'be_2']

for d in dirs:
    #MRS: add more explanatory information on this command
    results_protein = gmx.get_simulation_data(mdp=str(d) + '/protein.mdp',
                                              top=str(d) + '/trp-cage.top',
                                              edr=str(d) + '/run.edr',
                                              trr=str(d) + '/protein.trr')
    #MRS: document how to get this.
    results_protein.system.ndof_reduction_tra *= 2170.4375 / 96390.4017
    print('===> ' + d)

    #MRS: add comments on what the inputs mean, and some other options
    pv.kinetic_energy.equipartition(results_protein, filename='equipartition_'+str(d), verbosity=2)
