#!/usr/bin/env python3
"""
Setup script for fastoverlap package with enhanced error handling and platform detection.
"""

import platform
import sys
import subprocess
import shutil
from pathlib import Path

# For scikit-build-core, we don't import setup directly here
# The build-backend handles the setup process via pyproject.toml

def check_system_dependencies():
    """Check for required system dependencies."""
    errors = []

    # Check for cmake
    if not shutil.which("cmake"):
        errors.append("cmake is required but not found in PATH")

    # Check for pkg-config
    if not shutil.which("pkg-config"):
        errors.append("pkg-config is required but not found in PATH")

    # Check for FFTW and LAPACK via pkg-config
    try:
        subprocess.run(["pkg-config", "--exists", "fftw3"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        errors.append("FFTW3 library not found via pkg-config")

    try:
        subprocess.run(["pkg-config", "--exists", "lapack"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        # Try alternative LAPACK packages
        alt_lapack = ["openblas", "blas"]
        lapack_found = False
        for pkg in alt_lapack:
            try:
                subprocess.run(["pkg-config", "--exists", pkg], check=True, capture_output=True)
                lapack_found = True
                break
            except (subprocess.CalledProcessError, FileNotFoundError):
                continue

        if not lapack_found:
            errors.append("LAPACK/BLAS library not found via pkg-config")

    return errors

def print_platform_info():
    """Print platform information for debugging."""
    print(f"Platform: {platform.system()} {platform.release()}")
    print(f"Architecture: {platform.machine()}")
    print(f"Python: {sys.version}")

def main():
    """Main setup function with error handling."""
    print("Setting up fastoverlap...")
    print_platform_info()

    # Check system dependencies
    dep_errors = check_system_dependencies()
    if dep_errors:
        print("\nERROR: Missing system dependencies:")
        for error in dep_errors:
            print(f"  - {error}")
        print("\nPlease install the missing dependencies:")

        system = platform.system().lower()
        if system == "linux":
            print("  Ubuntu/Debian: sudo apt-get install cmake pkg-config libfftw3-dev liblapack-dev")
            print("  CentOS/RHEL: sudo yum install cmake pkgconfig fftw-devel lapack-devel")
            print("  Arch: sudo pacman -S cmake pkgconf fftw lapack")
        elif system == "darwin":
            print("  macOS: brew install cmake pkg-config fftw lapack")
        elif system == "windows":
            print("  Windows: Install cmake, pkg-config, and FFTW/LAPACK via vcpkg or conda")

        sys.exit(1)

    print("All system dependencies found!")

    print("Dependency check passed! Proceeding with build...")

def check_dependencies_only():
    """Check dependencies without building - for CI/CD systems."""
    print("Checking fastoverlap dependencies...")
    print_platform_info()

    dep_errors = check_system_dependencies()
    if dep_errors:
        print("\nERROR: Missing system dependencies:")
        for error in dep_errors:
            print(f"  - {error}")
        return False
    else:
        print("All system dependencies found!")
        return True

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--check-deps":
        success = check_dependencies_only()
        sys.exit(0 if success else 1)
    else:
        main()
