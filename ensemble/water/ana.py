#MRS: why set env here, not in other script? should be consistent to not confuse people
#!/usr/bin/env python3

# full documentation at http://physical-validation.readthedocs.io/
import physical_validation as pv

#MRS: is there a reason gmx_d vs. gmx? 
# setting the data parser. Needed if reading from GROMACS files.
# Place your gromacs binary and shared topology file here.
gmx = pv.data.GromacsParser(exe='gmx_d',
                            includepath='/usr/local/share/gromacs/top/')

algos = ['vr', 'be'] # two thermostats: velocity-rescaling and berendsen (weak-coupling)
ensembles = ['NVT', 'NPT'] # two ensembles: NVT and NPT
sims = {
    'NPT': 4, # we use 4 simulations for NPT: (T,P), (T+dT,P), (T,P+dP), (T+dT,P+dP)
    'NVT': 2  # we need 2 simulations for NVT: T and T+dT
}

results = {} # dictionary we will store the parsed data in
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
            #MRS: add comments: what do strict and verbosity do
            pv.kinetic_energy.distribution(results[a][e][-1], strict=False, verbosity=2)
            pv.kinetic_energy.distribution(results[a][e][-1], strict=False, verbosity=2,
                                           filename='_'.join(['ke', a, e, str(n)]))

        # add comments here on the inputs    
        if e == 'NVT':
            pv.ensemble.check(results[a][e][0], results[a][e][1], verbosity=2, filename='_'.join(['pe', a, e]))
        else:
            # there are three checks we can do: P(E_1)/P(E_2), P(V_1)/P(V_2) and P(E_1,V_1)/P(E_2,V_2)
            pv.ensemble.check(results[a][e][0], results[a][e][1], verbosity=2, filename='_'.join(['pe', a, e, 'dT']))
            pv.ensemble.check(results[a][e][0], results[a][e][2], verbosity=2, filename='_'.join(['pe', a, e, 'dP']))
            pv.ensemble.check(results[a][e][0], results[a][e][3], verbosity=2)
