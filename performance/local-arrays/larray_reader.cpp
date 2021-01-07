#include <adios2.h>
#include <cstdio>
#include <iostream>

std::vector<std::vector<double>> data_R64;

int validateData(int step, int idx, int rank, int size, int Nx) {
  double j = rank * Nx * 10 + step;
  int count = 0;

  for (int i = 0; i < Nx; i++) {
    if (data_R64[idx][i] != j + 10 * i) {
      count++;
    }
  }

  return (count);
}

int main(int argc, char **argv) {
  int rank, grank, comm_size;
  MPI_Comm comm;
  int writer_ranks;

  MPI_Init(NULL, NULL);

  MPI_Comm_rank(MPI_COMM_WORLD, &grank);
  MPI_Comm_split(MPI_COMM_WORLD, 2, grank, &comm);
  MPI_Comm_rank(comm, &rank);
  MPI_Comm_size(comm, &comm_size);

  int NSteps = 10;

  adios2::ADIOS adios(comm);
  adios2::IO io = adios.DeclareIO("TestIO");
  io.SetEngine("sst");
  adios2::Engine engine = io.Open("larray", adios2::Mode::Read);

  std::vector<double> rtime;
  MPI_Barrier(comm);
  double timeStart = MPI_Wtime();
  while (engine.BeginStep() == adios2::StepStatus::OK) {
    size_t writerSize;
    int t = engine.CurrentStep();

    auto var_r64 = io.InquireVariable<double>("r64");
    auto info = engine.BlocksInfo(var_r64, t);

    writer_ranks = info.size();

    int num_to_read = writer_ranks / comm_size;
    if (rank < (writer_ranks % comm_size))
      num_to_read++;
    data_R64.resize(num_to_read);

    for (int i = 0; i < num_to_read; i++) {
      int target_rank = rank + i * comm_size;
      int count = info.at(target_rank).Count[0];
      data_R64[i].resize(count);
      var_r64.SetBlockSelection(target_rank);
      engine.Get(var_r64, data_R64[i].data());
    }

    engine.EndStep();
    MPI_Barrier(comm);
    double timeEnd = MPI_Wtime();
    rtime.push_back(timeEnd - timeStart);
    if (rank == 0) {
      printf("step %d read in %f s\n", t, rtime[t]);
    }

    for (int i = 0; i < num_to_read; i++) {
      int target_rank = rank + i * comm_size;
      int count = info.at(target_rank).Count[0];
      if (validateData(t, i, target_rank, writer_ranks, count)) {
        fprintf(stderr,
                "Validation error for step %d of writer rank %d. (%d)\n", t,
                target_rank, rank);
      }
    }

    timeStart = MPI_Wtime();
  }

  engine.Close();

  MPI_Finalize();

  return (0);
}
