#include <adios2.h>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <iostream>

std::vector<double> data_R64;

void generateData(int step, int rank, int size, int Nx) {
  double j = rank * Nx * 10 + step;

  data_R64.resize(Nx);

  for (int i = 0; i < Nx; i++) {
    data_R64[i] = j + 10 * i;
  }
}

int main(int argc, char **argv) {
  int rank, grank, comm_size;
  ;
  MPI_Comm comm;
  MPI_Init(NULL, NULL);

  MPI_Comm_rank(MPI_COMM_WORLD, &grank);
  MPI_Comm_split(MPI_COMM_WORLD, 1, grank, &comm);
  MPI_Comm_rank(comm, &rank);
  MPI_Comm_size(comm, &comm_size);

  int local_array_size = 8;
  bool vary_size = false;

  for (int i = 1; i < argc; i++) {
    if (strcmp(argv[i], "-d") == 0) {
      vary_size = true;
    } else {
      local_array_size = atoi(argv[i]);
    }
  }

  std::size_t Nx = 10;
  int NSteps = 10;

  adios2::Dims count{static_cast<unsigned int>(Nx)};

  adios2::ADIOS adios(comm);
  adios2::IO io = adios.DeclareIO("TestIO");
  io.SetEngine("sst");
  adios2::Engine engine = io.Open("larray", adios2::Mode::Write);

  auto local_var_r64 = io.DefineVariable<double>("r64", {}, {}, count);
  const adios2::Mode sync = adios2::Mode::Deferred;

  std::vector<double> wtime(NSteps);

  int center = 1;
  for (size_t step = 0; step < NSteps; ++step) {
    // quiet bug if comm_size is a multiple of 35...who would ever do that?
    center = (center * ((comm_size % 5) ? 5 : 7)) % comm_size;
    // center is a misnomer
    int offset = center - (comm_size / 2);
    int rel_rank = (rank - offset) % comm_size;

    if (vary_size) {
      Nx = local_array_size * (1024 * 1024) + (1024 * 1024) * rel_rank;
    } else {
      Nx = local_array_size * (1024 * 1024);
    }
    generateData((int)step, rank, comm_size, (int)Nx);
    MPI_Barrier(comm);
    double timeStart = MPI_Wtime();
    engine.BeginStep();
    auto var_r64 = io.InquireVariable<double>("r64");
    adios2::Box<adios2::Dims> sel_size({}, {Nx});
    var_r64.SetSelection(sel_size);
    engine.Put(var_r64, data_R64.data(), sync);
    engine.EndStep();
    MPI_Barrier(comm);
    double timeEnd = MPI_Wtime();
    wtime[step] = timeEnd - timeStart;
    if (rank == 0) {
      printf("step %d written in %f s\n", (int)step, wtime[step]);
    }
  }

  engine.Close();

  MPI_Finalize();

  return (0);
}
