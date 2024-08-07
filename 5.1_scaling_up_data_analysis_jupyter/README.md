### SDSC Summer Institute 2024
# Session 5.1 Scaling up Interactive Data Analysis in Jupyter Lab: From Laptop to HPC

**Date:** Thursday, August 7, 2024

**Summary**: In this session we will demonstrate scaling up data analysis to larger than memory (out-of-core) datasets and processing them in parallel on CPU and GPU nodes. In the hands-on exercise we will compare Pandas, Dask, Spark, cuDF, and Dask-cuDF dataframe libraries for handling large datasets. We also cover setting up reproducible and transferable software environments for data analysis.

**Presented by:** [Peter Rose](https://www.sdsc.edu/research/researcher_spotlight/rose_peter.html) (pwrose @ucsd.edu)

### Reading and Presentations:
* **Lecture material:**
   * [Presentation Slides](5.1_SDSC_SI_2024.pdf)
   
   * [Ten simple rules](https://doi.org/10.1371/journal.pcbi.1007007) for writing and sharing computational analyses in Jupyter Notebooks

* **Source Code/Examples:**
   * Git Repository [df-parallel](https://github.com/sbl-sdsc/df-parallel): Comparison of Dataframe libraries for parallel processing of large tabular files


-----
## TASK 1: Launch Jupyter Lab on Expanse using a CONDA environment
1. Open a Terminal Window ("expanse Shell Access") through the [Expanse Portal Training Account](https://portal.expanse.sdsc.edu/training)

2. Clone the Git repository df-parallel in your home directory
```
git clone https://github.com/sbl-sdsc/df-parallel.git
```

3. Change into the df-parallel directory
```
cd df-parallel
```
  
4. Launch Jupyter Lab using the Galyleo script

   This script will generate a URL for your Jupyter Lab session.
```
galyleo launch --account ${SI24_ACCOUNT} --reservation ${SI24_RES_GPU} --qos ${SI24_QOS_GPU} --partition gpu-shared --cpus 10 --memory 92 --gpus 1 --time-limit 01:00:00 --conda-env df-parallel-gpu --conda-yml environment-gpu.yml --mamba
```

5. Open a new tab in your web browser and paste the Jupyter Lab URL. It may take a few minutes to launch your session.

> You should see the Satellite Reserver Proxy Service page launch in your browser.


------
## TASK 2: Benchmark Dataframe Libraries using a csv Input File

For this task you will compare the runtime for a simple data analysis using 5 dataframe libraries.

1. Go to the Jupyter Lab session

    Navigate to the ```df-parallel/notebooks``` directory.

2. Copy data files

    Run the ```1-FetchLocalData.ipynb``` notebook to copy two data sets of gene information (gene_info.tsv, gene_info.parquet) to the scratch disk on the GPU node.

3. Run the Dataframe notebooks with a csv input file

    Run the following Dataframe notebooks and write down the runtime shown at the bottom of each notebook.

```
2-PandasDataframe.ipynb
3-DaskDataframe.ipynb
4-SparkDataframe.ipynb
5-CudaDataframe.ipynb
6-DaskCudaDataframe.ipynb
```

> To get exact timings, run the notebook with the **```>>```** (Run All) button!
------

## TASK 3: Benchmark Dataframe Libraries using a Parquet Input File

In the following notebooks, change the file format to parquet: ```file_format = "parquet"``` and run them again. Write down the runtime shown at the bottom of each notebook. How does this compare with using csv files?
    
```
2-PandasDataframe.ipynb
5-CudaDataframe.ipynb
```
    
> To get exact timings, run the notebook with the **```>>```** (Run All) button!
------
    
## TASK 4: Measure Parallel Efficiency

In this task you will measure and plot the parallel efficiency of using a Dask dataframe with 1, 2, 4, and 8 cores. In the notebook below, select the file format ```parquet``` and the dataframe library ```Dask``` from the menu. Analyze the parallel efficiency plot and suggest how many cores would be ideal for this task.

```
7-ParallelEfficiency.ipynb
```
    
At the end of the session, don't forget to shutdown the process.

```
File -> Shutdown
``` 
------
