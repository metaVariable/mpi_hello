"""
HPC Base image

Contents:
  GNU compilers (upstream)
  OpenMPI version 2.1.2
"""
# pylint: disable=invalid-name, undefined-variable, used-before-assignment
devel_image = 'ubuntu:18.04'
runtime_image = 'ubuntu:18.04'

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
        ]
)

# GNU compilers
compiler = gnu()
Stage0 += compiler

# OpenMPI
Stage0 += openmpi(
    version='2.1.2',
    prefix='/usr/local/openmpi',
    cuda=False, 
    infiniband=False,
    configure_opts=[
        '--enable-mpi-cxx'
        ],
    toolchain=compiler.toolchain
)

# Compile Hello
Stage0 += copy(src='./mpi_hello.cpp', dest='/workspace/mpi_hello.cpp')
Stage0 += shell(commands=['cd /workspace', 'mpicxx mpi_hello.cpp -o mpi_hello'])

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
    src='/workspace/mpi_hello',
    dest='/workspace/mpi_hello',
)

Stage1 += environment(variables={'PATH': '$PATH:/workspace'})