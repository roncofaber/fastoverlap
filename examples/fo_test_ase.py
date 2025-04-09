#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  9 11:26:31 2025

@author: roncofaber
"""

import ase
import ase.build
import fastoverlap
from fastoverlap.sphericalAlignment import SphericalAlign, SphericalAlignFortran

#%%

mol1 = ase.build.molecule("H2O")
mol2 = ase.build.molecule("H2O")
mol2.rattle(0.3)


pos1 = mol1.get_positions()
pos2 = mol2.get_positions()

maxl  = 10
scale = 0.8

aligner_py  = SphericalAlign(scale=scale, Jmax=maxl)
aligner_fo  = SphericalAlignFortran(scale=scale, Jmax=maxl)

#Fastoverlap returns: distance, aligned cluster 1 and aligned cluster 2
res_py = aligner_py(pos1, pos2)
res_fo = aligner_fo(pos1, pos2)