### SDSC Summer Institute 2024
# Session 2.4 Batch Computing

**Date:** Monday, August 5, 2024

**Summary**: In this session on Batch Computing, we will introduce you to the concept of a distributed batch job scheduler — what they are, why they exist, and how they work — using the Slurm Workload Manager as our reference implementation and testbed. You will then learn how to write your first job script and submit it to an HPC System running Slurm as its scheduler. We will also discuss the best practices for how to structure your batch job scripts, teach you how to leverage Slurm environment variables, and provide tips on how to request resources from the scheduler to get your work done faster.

**Presented by:** [Marty Kandes](https://www.sdsc.edu/research/researcher_spotlight/thomas_mary.html) (mkandes @sdsc.edu)

### Reading and Presentations:
* **Lecture material:**
   * https://education.sdsc.edu/training/interactive/?id=202302-SDSCWebinar-Batch-Job-Scheduling-Slurm-Edition
   * https://education.sdsc.edu/training/interactive/?id=202403-Batch-Computing-Part-1
  
* **Source Code/Examples:** 
   * https://github.com/mkandes/batch-computing
 
   * 

### Clone the Repository

Next, let's clone the [4pi](https://github.com/mkandes/4pi) repo to your `HOME` directory on the HPC system.

*Command*

```
git clone https://github.com/mkandes/4pi.git
```

*Output*

```
[username@login01 ~]$ git clone https://github.com/mkandes/4pi.git
Cloning into '4pi'...
remote: Enumerating objects: 19, done.
remote: Counting objects: 100% (19/19), done.
remote: Compressing objects: 100% (10/10), done.
remote: Total 19 (delta 4), reused 19 (delta 4), pack-reused 0
Unpacking objects: 100% (19/19), 5.72 KiB | 7.00 KiB/s, done.
[username@login01 ~]$
```

### Your First Batch Job

To create your first batch job script, you'll need to open a new file in your text editor of choice.

```
[username@login01 ~]$ vi run-4pi.sh
```

```
#!/usr/bin/env bash

#SBATCH --job-name=my-first-4pi-test
#SBATCH --account=abc123
#SBATCH --partition=debug
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=1G
#SBATCH --time=00:05:00
#SBATCH --output=%x.o%j.%N

python3 pi.py 100000000


[Back to Top](#top)
