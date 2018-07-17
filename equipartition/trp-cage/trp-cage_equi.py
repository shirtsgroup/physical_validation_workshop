import physical_validation as pv


gmx = pv.data.GromacsParser(exe='/home/pascal/bin/gromacs/2018/single/bin/gmx',
                            includepath='/home/pascal/bin/gromacs/2018/single/share/gromacs/top/')

dirs = ['vr_1', 'vr_2', 'be_1', 'be_2']

for d in dirs:
    results_protein = gmx.get_simulation_data(mdp=str(d) + '/protein.mdp',
                                              top=str(d) + '/trp-cage.top',
                                              edr=str(d) + '/run.edr',
                                              trr=str(d) + '/protein.trr')
    results_protein.system.ndof_reduction_tra *= 2170.4375 / 96390.4017
    print('===> ' + d)
    pv.kinetic_energy.equipartition(results_protein, filename='equipartition_'+str(d), verbosity=2)
