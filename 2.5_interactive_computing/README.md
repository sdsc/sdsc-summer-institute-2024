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

**Summary**: Interactive computing refers to working with software that accepts input from the user as it runs. This applies not only to business and office applications, such as word processing and spreadsheet software, but HPC use cases involving code development, real-time data exploration and advanced visualizations run across one or more compute nodes. Interactive computing is often used when applications require large memory, have large data sets that are not that practical to download to local devices, need access to higher core counts or rely on software that is difficult to install. User inputs are entered via a command line interface (CLI) or application GUI (e.g., Jupyter Notebooks, Matlab, RStudio). Actions are initiated on remote compute nodes as a result of user inputs.  

This session will introduce participants to advanced CI concepts and what’s going on "under the hood" when they are using interactive tools.  Topics covered will include mechanisms for accessing interactive resources; commonalities and differences between batch and interactive computing; understanding the differences between web-based services and X11/GUI applications; monitoring jobs running on interactive nodes; overview of Open OnDemand portals.

**Presented by:** [Mary Thomas](https://www.sdsc.edu/research/researcher_spotlight/thomas_mary.html) (mpthomas @ucsd.edu)

### Reading and Presentations: <a name="docs"></a>
* **Lecture material:**
   * Presentation Slides: will be made available closer to the session
* **Source Code/Examples:** N/A
   * SDSC HPC Training Examples Repo @ https://github.com:sdsc-hpc-training-org/hpctr-examples.git
   * Expanse 101 tutorial: https://hpc-training.sdsc.edu/expanse-101/

[Back to Top](#top)
<hr>

### TASK 1: Clone the repo <a name="task1"></a>
* Update or clone the HPC-DSI24 Repository @ https://github.com/sdsc/sdsc-summer-institute-2024.git
* Clone the  SDSC HPC Training Examples Repo @ [https://github.com:sdsc-hpc-training-org/hpctr-examples.git](https://github.com:sdsc-hpc-training-org/hpctr-examples.git)

[Back to Top](#top)
<hr>

### TASK 2: Hands-on: Interactive Computing on CPU Node <a name="task2"></a>

#### On the day of the institute:
Use the __aliased__ command to obtain compute resources:
* for a CPU compute node use  ```srun-shared``` 
* for a GPU compute node use  ```srun-gpu-shared``` 

#### Use the srun command to get an interactive CPU node:

```
[mthomas@login02 calc-prime]$ srun --partition=compute  --pty --account=use300 --nodes=1 --ntasks-per-node=128 --mem=8G -t 00:30:00 --wait=0 --export=ALL /bin/bash
srun: job 24459379 queued and waiting for resources
srun: job 24459379 has been allocated resources
[mthomas@ ]$ cd hpctr-examples/calc-prime
[mthomas@exp-12-20 calc-prime]$
```

* Check the README.txt file for information about compiling and running the code:
**
```
[mthomas@exp-12-30 calc-prime]$ cat README.txt 
[1] Compile:

module purge 
module load slurm
module load cpu
module load gcc/10.2.0
module load openmpi/4.1.1

mpicc -o mpi_prime mpi_prime.c 


[2] Run as batch job:

    sbatch mpi-prime-slurm.sb

To pass value to script:
    sbatch --export=NHI=250000 mpi-prime-slurm.sb 

NOTE: for other compilers, replace "gcc"
with the one you want to use.
 
[3] Run using an interactive node:
Method [3a]
Request the interactive node using the "srun" command:

srun --partition=debug  --pty --account=use300 --nodes=1 --ntasks-per-node=24  --mem=8G -t 00:30:00 --wait=0 --export=ALL /bin/bash

Run the code using mpirun:
mpirun -n 64 ./mpi_prime 5000000

Method [3b]
Run job on an interactive node using the "salloc" command.
salloc - Obtain a Slurm job allocation (a set of nodes), execute a command, and then release the allocation when the command is finished.
For more information, see the Slurm page: https://slurm.schedmd.com/salloc.html

You can request resources using "salloc" and then use either "srun" or "mpirun" to run your MPI jobs. After you are done you can exit to relinquish the resources reserved by salloc. An example of using "salloc"

salloc --nodes=2 --ntasks-per-node=4 --cpus-per-task=2 -p debug --account=use300 -t 00:30:00 --mem=5G

Once you run this command, you will be on an interactive node, but the nodeID will not change. You can use 'srun' to execute your MPI code on the node:

srun --mpi=pmi2 -n 8 ./calc-prime
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

#### Compile and Run calc-prime from the command line

[mthomas@exp-12-30 calc-prime]$ mpicc -o mpi_prime mpi_prime.c 
[mthomas@exp-12-30 calc-prime]$ mpirun -np 8 ./mpi_prime 50000
The argument supplied is 50000
04 August 2024 04:34:52 PM

PRIME_MPI
 n_hi= 50000
  C/MPI version

  An MPI example program to count the number of primes.
  The number of processes is 8

         N        Pi          Time

         1         0        0.000764
         2         1        0.000004
         4         2        0.000003
         8         4        0.000003
        16         6        0.000003
        32        11        0.000003
        64        18        0.000004
       128        31        0.000005
       256        54        0.000010
       512        97        0.000031
      1024       172        0.000095
      2048       309        0.000328
      4096       564        0.001234
      8192      1028        0.004312
     16384      1900        0.015964
     32768      3512        0.059057

PRIME_MPI - Master process:
  Normal end of execution.

04 August 2024 04:34:52 PM

```

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

