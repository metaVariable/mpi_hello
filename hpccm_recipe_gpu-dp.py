"""
HPC Base image

Contents:
  CUDA version 10.0
  FFTW version 3.3.8
  GNU compilers (upstream)
  OpenMPI version 2.1.2
"""
# pylint: disable=invalid-name, undefined-variable, used-before-assignment
devel_image = 'nvidia/cuda:10.0-devel-ubuntu18.04'
runtime_image = 'nvidia/cuda:10.0-runtime-ubuntu18.04'

######
# Devel stage
######

Stage0.name = 'devel'

Stage0 += comment(__doc__, reformat=False)

Stage0 += baseimage(image=devel_image, _as='devel')

Stage0 += packages(
    apt=[
        'wget',
        'make',
        'cuda-samples-10-0'
        ]
)

# GNU compilers
compiler = gnu()
Stage0 += compiler

# FFTW
Stage0 += fftw(
    version='3.3.8', 
    prefix='/usr/local/fftw',
    configure_opts=[
            '--enable-float',
            '--enable-sse2'
            ],
    toolchain=compiler.toolchain
)

# OpenMPI
Stage0 += openmpi(
    version='2.1.2',
    prefix='/usr/local/openmpi',
    cuda=True, 
    infiniband=False,
    configure_opts=[
        '--enable-mpi-cxx'
        ],
    toolchain=compiler.toolchain
)

# MEGADOCK
Stage0 += copy(src='.', dest='/workspace')
Stage0 += copy(
    src='./docker/gpu-dp/Makefile',
    dest='/workspace/Makefile'
)

# Stage0 += workdir(directory='/workspace') # something wrong on workfir command
# Stage0 += shell(chdir=True, commands=['make -j$(nproc)']) # something wrong on workfir command
Stage0 += shell(commands=['cd /workspace', 'make -j$(nproc)'])

######
# Runtime image
######

Stage1.name = 'runtime'
Stage1 += baseimage(image=runtime_image, _as=Stage1.name)
Stage1 += Stage0.runtime(_from='devel')

Stage1 += workdir(directory='/workspace')

# copy MEGADOCK binary from devel
Stage1 += copy(
    _from=Stage0.name,
    src='/workspace/megadock-gpu-dp',
    dest='/workspace/megadock-gpu-dp',
)

Stage1 += environment(variables={'PATH': '$PATH:/workspace'})