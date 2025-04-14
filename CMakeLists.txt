cmake_minimum_required(VERSION 3.15)
project(fastoverlap LANGUAGES Fortran C CXX)

# add custom modules
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CMAKE_SOURCE_DIR}/cmake/findfftw")

# Find Python
find_package(Python REQUIRED COMPONENTS Interpreter Development.Module)

# Find pkg-config
find_package(PkgConfig REQUIRED)

# Find lapack and fftw
set(BLA_PREFER_PKGCONFIG 1)
find_package(LAPACK REQUIRED)
find_package(FFTW REQUIRED)

# Set Fortran compiler flags
set(CMAKE_Fortran_FLAGS "-w -O3 -march=native -funroll-loops -fPIC -fallow-argument-mismatch")

# Copy the fortran/ directory to the build/ directory
file(COPY ${CMAKE_SOURCE_DIR}/fastoverlap DESTINATION ${CMAKE_BINARY_DIR})

# Create the static library libqueue
set(QUEUE_FILE ${CMAKE_BINARY_DIR}/fastoverlap/f90/priorityqueue.f90)
add_library(queue STATIC ${QUEUE_FILE})

# Custom command to build Python extensions using f2py
add_custom_command(
    OUTPUT libbnb.so
    WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/fastoverlap/f90
    COMMAND
        ${Python_EXECUTABLE} -m numpy.f2py -c bnbalign.f90 commons.f90 alignutils.f90 -m libbnb
        -L${CMAKE_BINARY_DIR} -I${CMAKE_BINARY_DIR} -lqueue ${PKGC_LAPACK_LDFLAGS}
    DEPENDS queue
    COMMENT "Building libbnb Python extension with f2py"
)

add_custom_command(
    OUTPUT fastbulk.so
    WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/fastoverlap/f90
    COMMAND
        ${Python_EXECUTABLE} -m numpy.f2py -c fastbulk.f90 commons.f90 alignutils.f90 fastutils.f90 -m fastbulk
        -I${CMAKE_BINARY_DIR}/fastoverlap/f90 ${PKG_FFTW_LDFLAGS} ${PKGC_LAPACK_LDFLAGS}
    COMMENT "Building fastbulk Python extension with f2py"
)

add_custom_command(
    OUTPUT fastclusters.so
    WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/fastoverlap/f90
    COMMAND
        ${Python_EXECUTABLE} -m numpy.f2py -c fastclusters.f90 commons.f90 alignutils.f90 legendre.f90 DSOFT.f90 fastutils.f90 -m fastclusters
        -I${CMAKE_BINARY_DIR}/fastoverlap/f90 ${PKG_FFTW_LDFLAGS} ${PKGC_LAPACK_LDFLAGS}
    DEPENDS queue
    COMMENT "Building fastclusters Python extension with f2py"
)

# Custom targets to build the Python extensions
add_custom_target(f2py_libbnb       ALL DEPENDS libbnb.so)
add_custom_target(f2py_fastbulk     ALL DEPENDS fastbulk.so)
add_custom_target(f2py_fastclusters ALL DEPENDS fastclusters.so)

# Find and install the .so files to the fastoverlap/f90 directory within the site-packages directory
install(DIRECTORY ${CMAKE_BINARY_DIR}/fastoverlap/f90/
        DESTINATION ${CMAKE_INSTALL_PREFIX}/fastoverlap/f90
        FILES_MATCHING PATTERN "*.so")

# Install the Python files
file(GLOB PYTHON_FILES ${CMAKE_SOURCE_DIR}/fastoverlap/*.py)
file(GLOB PYTHON_F90_FILES ${CMAKE_SOURCE_DIR}/fastoverlap/f90/*.py)

# Install the Python files to the fastoverlap directory within the site-packages directory
install(FILES ${PYTHON_FILES}
        DESTINATION ${CMAKE_INSTALL_PREFIX}/fastoverlap)

# Install the Python files in the f90 directory to the fastoverlap/f90 directory within the site-packages directory
install(FILES ${PYTHON_F90_FILES}
        DESTINATION ${CMAKE_INSTALL_PREFIX}/fastoverlap/f90)