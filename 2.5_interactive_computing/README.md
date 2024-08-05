### SDSC Summer Institute 2024
# Session 2.5 Interactive Computing

**Date:** Monday, August 5, 2024

## Content:<a name="top">
* [Summary](summary)
* [Reading and Presentations:](docs)
* [Task 1: Clone the hpctrain repo](#task1)
* [Task 2: Hands-on: Interactive Computing on CPU Node](#task2)
* [Task 3: Hands-on: Interactive Computing on GPU Node](#task3)
* [Task 4: Jupyter Notebooks](#task4)
* [Task 5: Expanse Portal](#task5)
  
**Summary**: Interactive computing refers to working with software that accepts input from the user as it runs. This applies not only to business and office applications, such as word processing and spreadsheet software, but HPC use cases involving code development, real-time data exploration and advanced visualizations run across one or more compute nodes. Interactive computing is often used when applications require large memory, have large data sets that are not that practical to download to local devices, need access to higher core counts or rely on software that is difficult to install. User inputs are entered via a command line interface (CLI) or application GUI (e.g., Jupyter Notebooks, Matlab, RStudio). Actions are initiated on remote compute nodes as a result of user inputs.  

This session will introduce participants to advanced CI concepts and what’s going on "under the hood" when they are using interactive tools.  Topics covered will include mechanisms for accessing interactive resources; commonalities and differences between batch and interactive computing; understanding the differences between web-based services and X11/GUI applications; monitoring jobs running on interactive nodes; overview of Open OnDemand portals.

**Presented by:** [Mary Thomas](https://www.sdsc.edu/research/researcher_spotlight/thomas_mary.html) (mpthomas @ucsd.edu)

### Reading and Presentations: <a name="docs"></a>
* **Lecture material:**
   * Presentation Slides: will be made available closer to the session
* **Source Code/Examples:** 
   * SDSC HPC Training Examples Repo @ [https://github.com/sdsc-hpc-training-org/hpctr-examples](https://github.com/sdsc-hpc-training-org/hpctr-examples)
   * Expanse 101 tutorial: [https://hpc-training.sdsc.edu/expanse-101/](https://hpc-training.sdsc.edu/expanse-101/)

[Back to Top](#top)
<hr>

### TASK 1: Clone the HPC-DSI24 repo <a name="task1"></a>
* Update or clone the HPC-DSI24 Repository @ [https://github.com/sdsc/sdsc-summer-institute-2024.git](https://github.com/sdsc/sdsc-summer-institute-2024.git)
 * SDSC HPC Training Examples Repo @ [https://github.com/sdsc-hpc-training-org/hpctr-examples](https://github.com/sdsc-hpc-training-org/hpctr-examples)


[Back to Top](#top)
<hr>

### TASK 2: Hands-on: Interactive Computing on a CPU Node <a name="task2"></a>
When submitting a job to the batch queue, you use a script and submit the script to the queue. The job launches and runs your parallel code on the remote node in the background. This is not _interactive computing_. In this example you will learn to acquire a _compute node_, to compile your code on that node, and to run your parallel job from the command line.

#### On the day of the institute:
Use the __aliased__ command to obtain compute resources:
* for a CPU compute node use  ```srun-shared``` 
* for a GPU compute node use  ```srun-gpu-shared``` 

#### Use the srun command to get an interactive CPU node:

```
[mthomas@login02 calc-prime]$ srun --partition=compute  --pty --account=<<accnt_number>>  --nodes=1 --ntasks-per-node=128 --mem=8G -t 00:30:00 --wait=0 --export=ALL /bin/bash
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

* Set up the module ENV and check what you have available:

```
module purge 
module load slurm
module load cpu
module load gcc/10.2.0
module load openmpi/4.1.1

[mthomas@exp-6-16 calc-prime]$ module list
Currently Loaded Modules:
  1) slurm/expanse/21.08.8       3) gcc/10.2.0/npcyll4   5) openmpi/4.1.1/ygduf2r
  2) cpu/0.17.3b           (c)   4) ucx/1.10.1/dnpjjuc
  Where:
   c:  built natively for AMD Rome
```

#### Compile and Run calc-prime from the command line

```
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

[Back to Top](#top)
<hr>

### TASK 3: Hands-on: Interactive Computing on GPU Node <a name="task3"></a>

#### Use the srun command to get an interactive GPU node:

#### On the day of the institute:
Use the __aliased__ command to obtain compute resources:
* for a CPU compute node use  ```srun-shared``` 
* for a GPU compute node use  ```srun-gpu-shared``` 

#### Otherwise, use the command:

```
srun --partition=gpu-debug --pty --account=<<accnt_number>> --ntasks-per-node=10 --nodes=1 --mem=96G --gpus=1 -t 00:30:00 --wait=0 --export=ALL /bin/bash
```

* Check that you are on an NVIDIA GPU:

```
[mthomas@exp-7-59]$ cd hpctr-examples
[mthomas@exp-7-59 hpctr-examples]$ nvidia-smi
Sun Aug  4 17:04:30 2024       
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 525.85.12    Driver Version: 525.85.12    CUDA Version: 12.0     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|                               |                      |               MIG M. |
|===============================+======================+======================|
|   0  Tesla V100-SXM2...  On   | 00000000:18:00.0 Off |                    0 |
| N/A   35C    P0    41W / 300W |      0MiB / 32768MiB |      0%      Default |
|                               |                      |                  N/A |
+-------------------------------+----------------------+----------------------+
                                                                               
+-----------------------------------------------------------------------------+
| Processes:                                                                  |
|  GPU   GI   CI        PID   Type   Process name                  GPU Memory |
|        ID   ID                                                   Usage      |
|=============================================================================|
|  No running processes found                                                 |
+-----------------------------------------------------------------------------+
[mthomas@exp-7-59 hpctr-examples]$ 
 
```

* Move to the CUDA Hello World example, check the README file.

```
[mthomas@exp-7-59 hpctr-examples]$ cd cuda/hello-world
[mthomas@exp-7-59 hello-world]$ cat README.txt 
Hello World (GPU/CUDA)
------------------------------------------------------------------------
Updated by Mary Thomas (mthomas at ucsd.edu)
August, 2023
------------------------------------------------------------------------

[1] Load the correct modules for the CUDA Compiler:

module purge
module load gpu/0.15.4
module load gcc/7.2.0
module load cuda/11.0.2
module load slurm

[2] compile:
nvcc -o hello_world hello_world.cu

[3] run from interactive node
./hello_world
[mthomas@exp-7-59 hello-world]$
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

* compile and run hello-world

```
nvcc -o hello_world hello_world.cu
[mthomas@exp-7-59 hello-world]$ ./hello_world 
Hello,  SDSC HPC Training World!
[mthomas@exp-7-59 hello-world]$ 
```

* Try this for addition

```
[mthomas@exp-7-59 addition]$ cd ~/hpctr-examples/cuda/addition
[mthomas@exp-7-59 addition]$ nvcc -o add_gpu add_gpu.cu
[mthomas@exp-7-59 addition]$ ./add_gpu 

 Addition on CPU: 5 + 7 = 12

 Addition on GPU: 5 + 7 = 12

[mthomas@exp-7-59 addition]$ 

```


[Back to Top](#top)
<hr>

### TASK 4: Jupyter Notebooks<a name="task4"></a>
* running notebooks


[Back to Top](#top)
<hr>

### TASK 5: Log onto the Expanse Portal<a name="task5"></a>
* Simplifies your user environment -> useful for tasks that don't involve a lot of compiling and code development
* Web based access to your HPC System account, files, data, terminal connections, etc.
* Provides Web based access to interactive applications including Jupyter Notebooks & Jupyter Lab, Matlab, Rstudio.
* Access using your ACCESS portal account: https://github.com/user-attachments/assets/034cfd61-a0ef-4e24-b45e-e37c30cf2f4d



[Back to Top](#top)

