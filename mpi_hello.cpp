#include <iostream>
#include <mpi.h>
#include <stdio.h>

int main(int argc, char **argv)
{
  int rank, size;
  MPI_Init(&argc, &argv);
  // MPI::Init(argc, argv);

  MPI_Comm_rank(MPI_COMM_WORLD, &rank);
  MPI_Comm_size(MPI_COMM_WORLD, &size);
  // rank = MPI::COMM_WORLD.Get_rank();
  // size = MPI::COMM_WORLD.Get_size();

  std::cout << "rank = " << rank << std::endl;
  std::cout << "size = " << size << std::endl;

  MPI_Finalize();
  // MPI::Finalize();
}