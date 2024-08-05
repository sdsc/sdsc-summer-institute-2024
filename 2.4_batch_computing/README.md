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
   * https://github.com/mkandes/4pi

* **Link to Expanse User Portal:**
   * https://portal.expanse.sdsc.edu/training

Our first batch job script example.

```
#!/usr/bin/env bash

#SBATCH --job-name=my-first-job
#SBATCH --account=gue998
#SBATCH --partition=shared
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=1G
#SBATCH --time=00:05:00
#SBATCH --output=%x.o%j.%N

echo 'Hello, world!'
sleep 60
```
