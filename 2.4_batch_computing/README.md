### SDSC Summer Institute 2024
# Session 2.4 Batch Computing

**Date:** Monday, August 5, 2024

**Summary**: As computational and data requirements grow, researchers may find that they need to make the transition from dedicated resources (e.g., laptops, desktops) to campus clusters or nationally allocated systems. Jobs on these shared resources are typically executed under the control of a batch submission system such as Slurm, PBS, LSF or SGE. This requires a different mindset since the job needs to be configured so that the application(s) can be run non-interactively and at a time determined by the scheduler. The user also needs to specify the job duration, account information, hardware requirements and partition or queue. The goals of this session are to introduce participants to the fundamentals of batch computing before diving into the details of any particular workload manager to help them become more proficient, help ease porting of applications to different resources, and to allow CI Users to understand concepts such as fair share scheduling and backfilling.

**Presented by:** [Marty Kandes](https://www.sdsc.edu/research/researcher_spotlight/thomas_mary.html) (mkandes @sdsc.edu)

### Reading and Presentations:
* **Lecture material:**
   * Presentation Slides: Slides will be made available closer to the start of the session.
* **Source Code/Examples:** 
   * SDSC HPC Training Examples Repo @ [https://github.com/sdsc-hpc-training-org/hpctr-examples](https://github.com/sdsc-hpc-training-org/hpctr-examples)
   * Expanse 101 tutorial: https://hpc-training.sdsc.edu/expanse-101/

### TASKS: Hands-on
   * Clone the  SDSC HPC Training Examples Repo @ [https://github.com/sdsc-hpc-training-org/hpctr-examples](https://github.com/sdsc-hpc-training-org/hpctr-examples)
   * Run the following examples: env_info, mpi/hello-mpi, and calc-prime
   * Both the batch script and interactive commands should work
   * For more examples and in-depth Expanse tutorial, see https://hpc-training.sdsc.edu/expanse-101/
   * Practice passing variables into the batch script from the command line

[Back to Top](#top)
