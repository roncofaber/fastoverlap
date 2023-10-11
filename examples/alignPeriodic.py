# -*- coding: utf-8 -*-

import os
import csv
import numpy as np
from fastoverlap import PeriodicAlign
try:
    from fastoverlap import PeriodicAlignFortran, BranchnBoundAlignment
    fortran=True
except ImportError:
    fortran=False

datafolder = "BLJ256/"

def readFile(filename):
    with open(filename, 'rb') as f:
        reader = csv.reader(f, delimiter=' ')
        dist = [list(map(float, row)) for row in reader]
    return np.array(dist)

pos1 = np.loadtxt(os.path.join(datafolder, 'coords'))
pos2 = np.loadtxt(os.path.join(datafolder, 'finish'))

natoms = 256
ntypeA = 204
shape = (natoms, 3)
boxVec = np.ones(3)*5.975206329 #(natoms/1.2)**(1./3.)
permlist = [np.arange(ntypeA), np.arange(ntypeA, natoms)]
align = PeriodicAlign(natoms, boxVec, permlist)

if fortran:
    alignf = PeriodicAlignFortran(natoms, boxVec, permlist)
    bnb = BranchnBoundAlignment(invert=False,boxSize=boxVec, perm=permlist)

c1, c2 = (align.calcFourierCoeff(p) for p in (pos1, pos2))

def quickAlign(c1, c2):
    """
    If fourier coefficients, c1 and c2 are precalculated the algorithm
    runs faster
    """
    return align.align(pos1, pos2, [c1,c2])

if __name__ == "__main__":
    print("starting")
    permRMS = align.Hungarian(pos1, pos2)[0]*natoms**-0.5
    print('Performing permutational alignment with Hungarian algorithm')
    print('RMSD = {:0.4f}'.format(permRMS))

    print('Performing fastoverlap alignment')
    dist, X1, X2, perm, disp = align(pos1, pos2)
    fastRMS = dist*natoms**-0.5
    print('RMSD = {:0.4f}'.format(fastRMS))

    if fortran:
        print('Performing fortran fastoverlap alignment')
        dist, X1, X2, perm = alignf(pos1, pos2)
        fastRMS = dist*natoms**-0.5
        print('RMSD = {:0.4f}'.format(fastRMS))

        print('Performing branch and bound alignment')
        dist, X1, X2 = bnb(pos1, pos2, niter=100)
        bnbRMS = dist*natoms**-0.5
        print('RMSD = {:0.4f}'.format(bnbRMS))

    import timeit
    print('Timing fastoverlap alignment:')

    alignTimer = timeit.Timer(stmt="palign.align(palign.pos1, palign.pos2)",
                     setup="import alignPeriodic as palign")
    aligntime =  alignTimer.timeit(10)/10.

    fastTimer = timeit.Timer(stmt="palign.quickAlign(palign.c1, palign.c2)",
                     setup="import alignPeriodic as palign")
    fasttime = fastTimer.timeit(10)/10.

    print('Average time to align for fast overlap {:0.3} s'.format(aligntime))
    print('Average time to align with precalculated coefficients {:0.3} s'.format(fasttime))

    if fortran:
        fTimer = timeit.Timer(stmt="palign.alignf(palign.pos1, palign.pos2,1)",
                         setup="import alignPeriodic as palign")
        ftime =  alignTimer.timeit(10)/10.

        bnbTimer = timeit.Timer(stmt="palign.bnb(palign.pos1, palign.pos2, niter=100)",
                         setup="import alignPeriodic as palign")
        bnbtime = bnbTimer.timeit(10)/10.

        print('Average time to align for fortran fast overlap {:0.3} s'.format(ftime))
        print('Average time to align for branch and bound alignment {:0.3} s'.format(bnbtime))

