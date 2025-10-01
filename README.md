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

## System Requirements

### Python Requirements:
- Python 3.8 or higher
- The package has been tested on Python 3.8-3.12

### System Dependencies:

Before installation, ensure you have the following system dependencies installed:

**Ubuntu/Debian:**
```bash
sudo apt-get install cmake pkg-config libfftw3-dev liblapack-dev gfortran
```

**CentOS/RHEL:**
```bash
sudo yum install cmake pkgconfig fftw-devel lapack-devel gcc-gfortran
```

**Arch Linux:**
```bash
sudo pacman -S cmake pkgconf fftw lapack gcc-fortran
```

**macOS (with Homebrew):**
```bash
brew install cmake pkg-config fftw lapack gcc
```

**Windows:**
- Install cmake, pkg-config, and FFTW/LAPACK via vcpkg or conda
- Consider using conda environment for easier dependency management

### Python Dependencies:

The package automatically installs the following Python dependencies:
- `numpy>=1.19.0,<2.0.0`: numerical computing and f2py for Fortran compilation
- `scipy>=1.5.0`: scientific computing tools and optimizers
- `munkres>=1.1.0`: linear assignment problem solver for permutational alignment

## Installation Methods

### 1. Standard Installation (Recommended)

The easiest way to install fastoverlap:

```bash
# Basic installation
pip install -e .

# Or for a regular (non-editable) install
pip install .
```

### 2. Installation with Optional Dependencies

For different use cases, you can install with optional dependencies:

```bash
# Install with ASE support (for examples)
pip install -e ".[examples]"

# Install with development tools
pip install -e ".[dev]"

# Install everything
pip install -e ".[all]"
```

### 3. Check Dependencies Before Installation

You can check if all system dependencies are available before attempting installation:

```bash
python setup.py --check-deps
```

This will report any missing system dependencies and provide installation instructions for your platform.

### 4. Alternative Installation via requirements.txt

If you prefer using requirements.txt:

```bash
pip install -r requirements.txt
pip install -e .
```

### 5. Manual Installation (Fallback)

If pip installation fails, you can manually build the package:

```bash
# Clone the repository
git clone https://github.com/roncofaber/fastoverlap.git
cd fastoverlap/

# Create build directory
mkdir build
cd build/

# Configure and build
cmake ..
make -j4  # Use multiple cores for faster compilation

# Optional: Install to system Python packages
make install
```

## Troubleshooting Installation

### Common Issues:

1. **Missing system dependencies**: Run `python setup.py --check-deps` to identify missing packages
2. **Fortran compiler issues**: Install `gfortran` and ensure it's in your PATH
3. **NumPy 2.0 compatibility**: The package is pinned to numpy<2.0.0 for stability
4. **Permission errors**: Use `--user` flag with pip or create a virtual environment

### Virtual Environment (Recommended)

For a clean installation, use a virtual environment:

```bash
# Create virtual environment
python -m venv fastoverlap_env

# Activate it
source fastoverlap_env/bin/activate  # Linux/macOS
# or
fastoverlap_env\Scripts\activate  # Windows

# Install
pip install -e .
```

### Conda Environment

For conda users:

```bash
# Create conda environment with dependencies
conda create -n fastoverlap python=3.11 cmake numpy scipy
conda activate fastoverlap

# Install remaining dependencies
conda install -c conda-forge fftw pkg-config

# Install package
pip install -e .
```

## Verification

After installation, verify everything works:

```bash
# Test basic functionality
python examples/fo_test_ase.py

# Check available Fortran modules
python -c "import fastoverlap.f90 as f90; print(f'Fortran modules available: {f90.have_fortran}')"
```





