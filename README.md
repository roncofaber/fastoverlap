# DISCLAIMER
This is a fork of the GitHub FASTOVERLAP package by M. Griffiths that can be found at [here](https://github.com/matthewghgriffiths/fastoverlap). The original repo was modified to work with newer Python versions and with the [`sea_urchin` MD analysis code](https://gitlab.com/electrolyte-machine/sea_urchin).

**Changes from original repo:**
- Building of the the fortran extensions using `f2py` does not rely on the deprecated `numpy.distutils`, but rather on `cmake` and `meson`. This makes it compatible with newer Python versions.
- `cmake` should automatically detect the needed `lapack` and `fftw` libraries for multiple architectures.
- `SphericalAlignFortran` has been changed to return the permutation vector used by the alignment and the inversion operator (+1 or -1). `SphericalAlign` does not have this change yet (WIP)
- Few other minor changes to `.f90` filesto ensure this compiles _smooth_.


# FASTOVERLAP
Algorithms for fast alignment of structures in finite and periodic systems. These methods are also implemented in the [Cambridge Energy Landscape Software](http://www-wales.ch.cam.ac.uk/software.html) in `GMIN` and `OPTIM`.

FASTOVERLAP can be run 'as is' with no compilation required using `PeriodicAlign` and `SphericalAlign`. The Fortran modules need to be compiled to peform branch and bound alignments with `BranchnBoundAlignment`. 

These algorithms have been detailed in the paper,

**Optimal Alignment of Structures for Finite and Periodic Systems** Matthew Griffiths, Samuel P. Niblett, and David J. Wales _Journal of Chemical
Theory and Computation_ **2017** 13(10), 4914-4931, doi:[10.1021/acs.jctc.7b00543](http://dx.doi.org/10.1021/acs.jctc.7b00543)

If you use this module, please cite the above paper.

![Difference between FASTOVERLAP (maximising overlap) vs Branch and Bound Alignment (minimising RMSD)](./alignment.gif)

# INSTALLATION

## Required packages

### Python (3.8+) packages:

1. `numpy`: we use numpy everywhere for doing numerical work. It also installs `f2py` which is used to compile fortran code into modules callable by python.
2. `scipy`: for some of the optimizers and various scientific tools.
3. [`munkres`](https://pypi.org/project/munkres/) (preferred) or [`pele`](http://pele-python.github.io/pele/): to solve the linear assignment problem for permutational alignment.

### Fortran compilation:

1. Fortran compiler (tested with `gfortran`).
2. Scientific libraries: `fftw` and `lapack` (on Ubutnu install from apt liblapack-dev and libfftw3-dev).
3. `cmake` and `meson` to build the fortran extensions.

## Compilation instruction

### Install using `pip`

Often, you can just use pip to install in one of the following modes:

```bash
# Simple install:
pip install .

# Install in development mode
pip install -e .
```


### Manual installation

In some cases, the pip installation can fail. In that case you can manually install the package:

```bash
# clone the repo
git clone https://github.com/roncofaber/fastoverlap.git
cd fastoverlap/

# create build directory
mkdir build
cd build/

# compile
cmake ..
make # -j 4 for parallel

# optional (will copy the files in your python packages folder)
make install
```

If you don't want to run `make install`, you can add the `build` directory to your `PYTHONPATH`, or copy the `*.so` extensions from `fastoverlap/build/fastoverlap/f90` to `fastoverlap/fastoverlap/f90` and add the cloned repo to the `PYTHONPATH`.





