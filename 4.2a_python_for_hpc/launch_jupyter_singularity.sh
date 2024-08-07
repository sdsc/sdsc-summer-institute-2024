export PATH="/cm/shared/apps/sdsc/galyleo:${PATH}"
SIMG='/expanse/lustre/projects/sds166/zonca/dask-numba-si24.sif'
# Summer institute account
# Use current folder
NOTEBOOK_FOLDER=$(pwd -P)
# Create link
cd 1_dask_tutorial
rm -f data
ln -s /expanse/lustre/projects/sds166/zonca/dask_tutorial_data data
cd ../
# Use the user home
# NOTEBOOK_FOLDER=${HOME}

## Debug
#galyleo launch --account ${SI24_ACCOUNT} --partition debug --cpus 128 --memory 243 --time-limit 00:30:00 --env-modules singularitypro --jupyter 'lab' --notebook-dir "${NOTEBOOK_FOLDER}" --sif ${SIMG} --bind '/cm,/expanse,/scratch' --quiet

galyleo launch --reservation ${SI24_RES_CPU} --account ${SI24_ACCOUNT} --partition compute --cpus 128 --memory 243 --time-limit 04:00:00 --env-modules singularitypro --jupyter 'lab' --notebook-dir "${NOTEBOOK_FOLDER}" --sif ${SIMG} --bind '/cm,/expanse,/scratch' --quiet
