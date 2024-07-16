### SDSC Summer Institute 2024
# Session 2.5 Interactive Computing

**Date:** Monday, August 5, 2024

## Content:<a name="top">
* [Summary](summary)
* [Reading and Presentations:](docs)
* [Task 1: Clone the repo](#task1)
* [Task 2: Hands-on: Interactive Computing on CPU Node](#task2)
* [Task 3: Hands-on: Interactive Computing on GPU Node](#task3)
* [Task 4: Hands-on: Run GnuPlot on CPU](#task4)
* [Task 5: Examine NetCDF data on CPU](#task5)

**Summary**: Interactive computing refers to working with software that accepts input from the user as it runs. This applies not only to business and office applications, such as word processing and spreadsheet software, but HPC use cases involving code development, real-time data exploration and advanced visualizations run across one or more compute nodes. Interactive computing is often used when applications require large memory, have large data sets that are not that practical to download to local devices, need access to higher core counts or rely on software that is difficult to install. User inputs are entered via a command line interface (CLI) or application GUI (e.g., Jupyter Notebooks, Matlab, RStudio). Actions are initiated on remote compute nodes as a result of user inputs.  This session will introduce participants to advanced CI concepts and what’s going on "under the hood" when they are using interactive tools.  Topics covered will include mechanisms for accessing interactive resources; commonalities and differences between batch and interactive computing; understanding the differences between web-based services and X11/GUI applications; monitoring jobs running on interactive nodes; overview of Open OnDemand portals.

**Presented by:** [Mary Thomas](https://www.sdsc.edu/research/researcher_spotlight/thomas_mary.html) (mpthomas @ucsd.edu)

### Reading and Presentations: <a name="docs"></a>
* **Lecture material:**
   * Presentation Slides: will be made available closer to the session
* **Source Code/Examples:** N/A
   * SDSC HPC Training Examples Repo @ [https://github.com:sdsc-hpc-training-org/hpctr-examples.git](https://github.com:sdsc-hpc-training-org/hpctr-examples.git)
   * Expanse 101 tutorial: https://hpc-training.sdsc.edu/expanse-101/

[Back to Top](#top)
<hr>

### TASK 1: Clone the repo <a name="task1"></a>
   * Clone the  SDSC HPC Training Examples Repo @ [https://github.com:sdsc-hpc-training-org/hpctr-examples.git](https://github.com:sdsc-hpc-training-org/hpctr-examples.git)

[Back to Top](#top)
<hr>

### TASK 2: Hands-on: Interactive Computing on CPU Node <a name="task2"></a>
#### Use the srun command to get an interactive CPU node:

```
[mthomas@login02 calc-prime]$ srun --partition=compute  --pty --account=use300 --nodes=1 --ntasks-per-node=128 --mem=8G -t 00:30:00 --wait=0 --export=ALL /bin/bash
srun: job 24459379 queued and waiting for resources
srun: job 24459379 has been allocated resources
[mthomas@exp-6-16 calc-prime]$
```

* Set up the module ENV:

```
module purge 
module load slurm
module load cpu
module load gcc/10.2.0
module load openmpi/4.1.1
```

* list the modules

```
[mthomas@exp-6-16 calc-prime]$ module list
Currently Loaded Modules:
  1) slurm/expanse/21.08.8       3) gcc/10.2.0/npcyll4   5) openmpi/4.1.1/ygduf2r
  2) cpu/0.17.3b           (c)   4) ucx/1.10.1/dnpjjuc
  Where:
   c:  built natively for AMD Rome
```

#### Run calc-prime from the command line

```
mpirun -np 16 ./mpi_prime 500000
07 August 2023 01:36:28 AM

PRIME_MPI
 n_hi= 262144
  C/MPI version

  An MPI example program to count the number of primes.
  The number of processes is 16

         N        Pi          Time

         1         0        0.000817
         2         1        0.000583
         4         2        0.000004
         8         4        0.000004
        16         6        0.000004
        32        11        0.000004
        64        18        0.000004
       128        31        0.000005
       256        54        0.000008
       512        97        0.000018
      1024       172        0.000054
      2048       309        0.000189
      4096       564        0.000638
      8192      1028        0.002281
     16384      1900        0.008125
     32768      3512        0.029826
     65536      6542        0.111391
    131072     12251        0.415458
    262144     23000        1.543699
    524288     43390       23.354061

PRIME_MPI - Master process:
  Normal end of execution.

07 August 2023 01:44:11 AM
```

[Back to Top](#top)
<hr>

### TASK 3: Hands-on: Interactive Computing on GPU Node <a name="task3"></a>

#### Use the srun command to get an interactive GPU node:

```
srun --partition=gpu-debug --pty --account=use300 --ntasks-per-node=10 --nodes=1 --mem=96G --gpus=1 -t 00:30:00 --wait=0 --export=ALL /bin/bash
```

* Check that you are on an NVIDIA GPU:

```
[mthomas@exp-7-59 mpi]$ nvidia-smi
Mon Aug  7 01:51:59 2023       
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 515.65.01    Driver Version: 515.65.01    CUDA Version: 11.7     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|                               |                      |               MIG M. |
|===============================+======================+======================|
|   0  Tesla V100-SXM2...  On   | 00000000:18:00.0 Off |                    0 |
| N/A   34C    P0    41W / 300W |      0MiB / 32768MiB |      0%      Default |
|                               |                      |                  N/A |
+-------------------------------+----------------------+----------------------+
                                                                               
+-----------------------------------------------------------------------------+
| Processes:                                                                  |
|  GPU   GI   CI        PID   Type   Process name                  GPU Memory |
|        ID   ID                                                   Usage      |
|=============================================================================|
|  No running processes found                                                 |
+-----------------------------------------------------------------------------+
[mthomas@exp-7-59 mpi]$ 
```

* Set up the module ENV:

```
module purge
module load gpu/0.15.4
module load gcc/7.2.0
module load cuda/11.0.2
module load slurm
[mthomas@exp-7-59 hello-world]$ module list
Currently Loaded Modules:
  1) gpu/0.15.4 (g)   2) gcc/7.2.0   3) cuda/11.0.2   4) slurm/expanse/21.08.8

  Where:
   g:  built natively for Intel Skylake
```

* cd to cuda/hello-world directory
* compile hello-world

```
nvcc -o hello_world hello_world.cu
```

* Run the hello-world applciation

```
[mthomas@exp-7-59 hello-world]$ ./hello_world 
Hello,  SDSC HPC Training World!
[mthomas@exp-7-59 hello-world]$ 
```

* Try this for addition

[Back to Top](#top)
<hr>

### TASK 4: Hands-on: Run GnuPlot on CPU<a name="task4"></a>

[Back to Top](#top)
<hr>

### TASK 5: Examine NetCDF data on CPU<a name="task5"></a>


[Back to Top](#top)

