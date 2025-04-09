cmake_minimum_required(VERSION 3.15)
project(fastoverlap LANGUAGES Fortran C CXX)

# Find Python
find_package(Python REQUIRED COMPONENTS Interpreter Development.Module)

# Find required libraries
find_package(LAPACK REQUIRED)
find_package(BLAS REQUIRED)

# Find FFTW3
find_package(PkgConfig QUIET)
if(PkgConfig_FOUND)
    pkg_check_modules(FFTW3 IMPORTED_TARGET fftw3)
endif()

if(NOT FFTW3_FOUND)
    # Manual FFTW3 detection as fallback
    find_library(FFTW3_LIBRARIES NAMES fftw3 fftw3f)
    find_path(FFTW3_INCLUDE_DIRS NAMES fftw3.h)
    if(FFTW3_LIBRARIES AND FFTW3_INCLUDE_DIRS)
        set(FFTW3_FOUND TRUE)
    else()
        message(FATAL_ERROR "FFTW3 library not found. Please install FFTW3 or specify its location.")
    endif()
endif()

# Set Fortran compiler flags
set(CMAKE_Fortran_FLAGS "${CMAKE_Fortran_FLAGS} -Wall -funroll-loops -O3 -march=native -Wrestrict")

# Create build directory for the compiled libraries
file(MAKE_DIRECTORY ${CMAKE_BINARY_DIR}/fastoverlap/f90)

# Create a common module directory
file(MAKE_DIRECTORY ${CMAKE_BINARY_DIR}/modules)

# Function to analyze Fortran file dependencies
function(analyze_fortran_dependencies file_path modules_provided modules_used)
    # Extract modules provided by this file
    execute_process(
        COMMAND bash -c "grep -i '^\\s*module\\s\\+[a-z0-9_]\\+' '${file_path}' | sed 's/.*module\\s\\+\\([a-z0-9_]\\+\\).*/\\1/i'"
        OUTPUT_VARIABLE provided
        OUTPUT_STRIP_TRAILING_WHITESPACE
    )
    string(REPLACE "\n" ";" provided_list "${provided}")
    set(${modules_provided} ${provided_list} PARENT_SCOPE)
    
    # Extract modules used by this file
    execute_process(
        COMMAND bash -c "grep -i '^\\s*use\\s\\+[a-z0-9_]\\+' '${file_path}' | sed 's/.*use\\s\\+\\([a-z0-9_]\\+\\).*/\\1/i'"
        OUTPUT_VARIABLE used
        OUTPUT_STRIP_TRAILING_WHITESPACE
    )
    string(REPLACE "\n" ";" used_list "${used}")
    set(${modules_used} ${used_list} PARENT_SCOPE)
endfunction()

# Get all Fortran source files
file(GLOB FORTRAN_SOURCES ${CMAKE_CURRENT_SOURCE_DIR}/fastoverlap/f90/*.f90)

# Create a map of which file provides which module
set(MODULE_PROVIDERS)
foreach(SOURCE_FILE ${FORTRAN_SOURCES})
    analyze_fortran_dependencies(${SOURCE_FILE} MODULES_PROVIDED MODULES_USED)
    foreach(MODULE ${MODULES_PROVIDED})
        set(MODULE_PROVIDERS_${MODULE} ${SOURCE_FILE})
        list(APPEND MODULE_PROVIDERS ${MODULE})
    endforeach()
endforeach()

# Create a topologically sorted list of files based on dependencies
set(SORTED_FILES)
set(VISITED_FILES)

function(visit_file file)
    list(FIND VISITED_FILES ${file} VISITED)
    if(NOT ${VISITED} EQUAL -1)
        return()
    endif()
    
    list(APPEND VISITED_FILES ${file})
    set(VISITED_FILES ${VISITED_FILES} PARENT_SCOPE)
    
    analyze_fortran_dependencies(${file} MODULES_PROVIDED MODULES_USED)
    
    foreach(MODULE ${MODULES_USED})
        if(DEFINED MODULE_PROVIDERS_${MODULE})
            visit_file(${MODULE_PROVIDERS_${MODULE}})
        endif()
    endforeach()
    
    list(APPEND SORTED_FILES ${file})
    set(SORTED_FILES ${SORTED_FILES} PARENT_SCOPE)
endfunction()

foreach(SOURCE_FILE ${FORTRAN_SOURCES})
    visit_file(${SOURCE_FILE})
endforeach()

# Remove duplicates from the sorted list
list(REMOVE_DUPLICATES SORTED_FILES)

# Print the dependency order for debugging
message(STATUS "Fortran files in dependency order:")
foreach(FILE ${SORTED_FILES})
    get_filename_component(FILENAME ${FILE} NAME)
    message(STATUS "  ${FILENAME}")
endforeach()

# Create a single library with all Fortran modules
add_library(fortran_modules STATIC ${SORTED_FILES})
set_target_properties(fortran_modules PROPERTIES
    Fortran_MODULE_DIRECTORY ${CMAKE_BINARY_DIR}/modules
)

# Link dependencies to the module library
if(FFTW3_FOUND)
    if(TARGET PkgConfig::FFTW3)
        target_link_libraries(fortran_modules PRIVATE PkgConfig::FFTW3)
    else()
        target_include_directories(fortran_modules PRIVATE ${FFTW3_INCLUDE_DIRS})
        target_link_libraries(fortran_modules PRIVATE ${FFTW3_LIBRARIES})
    endif()
endif()
target_link_libraries(fortran_modules PRIVATE ${LAPACK_LIBRARIES} ${BLAS_LIBRARIES})

# Create Python extension modules
# Each will use the pre-compiled modules
Python_add_library(fastbulk MODULE WITH_SOABI)
target_sources(fastbulk PRIVATE fastoverlap/f90/fastbulk.f90)
target_include_directories(fastbulk PRIVATE ${CMAKE_BINARY_DIR}/modules)
target_link_libraries(fastbulk PRIVATE fortran_modules ${LAPACK_LIBRARIES} ${BLAS_LIBRARIES})
if(FFTW3_FOUND)
    if(TARGET PkgConfig::FFTW3)
        target_link_libraries(fastbulk PRIVATE PkgConfig::FFTW3)
    else()
        target_include_directories(fastbulk PRIVATE ${FFTW3_INCLUDE_DIRS})
        target_link_libraries(fastbulk PRIVATE ${FFTW3_LIBRARIES})
    endif()
endif()

Python_add_library(fastclusters MODULE WITH_SOABI)
target_sources(fastclusters PRIVATE fastoverlap/f90/fastclusters.f90)
target_include_directories(fastclusters PRIVATE ${CMAKE_BINARY_DIR}/modules)
target_link_libraries(fastclusters PRIVATE fortran_modules ${LAPACK_LIBRARIES} ${BLAS_LIBRARIES})
if(FFTW3_FOUND)
    if(TARGET PkgConfig::FFTW3)
        target_link_libraries(fastclusters PRIVATE PkgConfig::FFTW3)
    else()
        target_include_directories(fastclusters PRIVATE ${FFTW3_INCLUDE_DIRS})
        target_link_libraries(fastclusters PRIVATE ${FFTW3_LIBRARIES})
    endif()
endif()

Python_add_library(libbnb MODULE WITH_SOABI)
target_sources(libbnb PRIVATE fastoverlap/f90/bnbalign.f90)
target_include_directories(libbnb PRIVATE ${CMAKE_BINARY_DIR}/modules)
target_link_libraries(libbnb PRIVATE fortran_modules ${LAPACK_LIBRARIES} ${BLAS_LIBRARIES})

# Set output names and properties
set_target_properties(fastbulk PROPERTIES 
    OUTPUT_NAME fastoverlap/f90/fastbulk
    LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR})

set_target_properties(fastclusters PROPERTIES 
    OUTPUT_NAME fastoverlap/f90/fastclusters
    LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR})

set_target_properties(libbnb PROPERTIES 
    OUTPUT_NAME fastoverlap/f90/libbnb
    LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR})

# Install Python package
install(DIRECTORY fastoverlap/ DESTINATION fastoverlap
        FILES_MATCHING PATTERN "*.py")

# Install compiled extensions
install(TARGETS fastbulk fastclusters libbnb
        LIBRARY DESTINATION fastoverlap/f90)
