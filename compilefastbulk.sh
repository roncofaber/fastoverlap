cd ./fastoverlap/f90
f2py -c fastbulk.f90 -m fastbulk --link-lapack --link-fftw
