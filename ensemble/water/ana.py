#!/usr/bin/env python3

import physical_validation as pv


gmx = pv.data.GromacsParser(exe='/home/pascal/bin/gromacs/2018/double/bin/gmx_d',
                            includepath='/home/pascal/bin/gromacs/2018/double/share/gromacs/top/')

algos = ['vr', 'be']
ensembles = ['NVT', 'NPT']
sims = {
    'NPT': 4,
    'NVT': 2
}

results = {}
for a in algos:
    results[a] = {}
    for e in ensembles:
        results[a][e] = []
        for n in range(1, sims[e]+1):
            d = 'md_' + e + '_' + a + '_' + str(n) + '/'
            results[a][e].append(
                gmx.get_simulation_data(
                    mdp=d + 'mdout.mdp',
                    top='top/system.top',
                    edr=d + 'system.edr',
                    gro=d + 'system.gro'
                )
            )
            pv.kinetic_energy.distribution(results[a][e][-1], strict=False, verbosity=2)
            pv.kinetic_energy.distribution(results[a][e][-1], strict=False, verbosity=2,
                                           filename='_'.join(['ke', a, e, str(n)]))

        if e == 'NVT':
            pv.ensemble.check(results[a][e][0], results[a][e][1], verbosity=2, filename='_'.join(['pe', a, e]))
        else:
            pv.ensemble.check(results[a][e][0], results[a][e][1], verbosity=2, filename='_'.join(['pe', a, e, 'dT']))
            pv.ensemble.check(results[a][e][0], results[a][e][2], verbosity=2, filename='_'.join(['pe', a, e, 'dP']))
            pv.ensemble.check(results[a][e][0], results[a][e][3], verbosity=2)
