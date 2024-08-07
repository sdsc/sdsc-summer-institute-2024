# ----------------------------------------------------------------------------
# Exercise: running MNIST CNN with multinode using Horovod
#
# The coding changes are based on documentation for Tensorflow V2 Keras example at https://horovod.readthedocs.io/en/latest/keras.html 
#
# 1
# Review the code below 
#

# 2
# Do a File->open of the run-hvd-main-cpu2.sb slurm batch script
#       optionally edit the number of cpus to use, try for example 4,8,16, and/or 32
# 3
# In a terminal window, submit the script and review the job status
#          ]$  sbatch run-hvd-main-cpu2.sb
#          ]$  squeue -u your-userid
#      
# Optionally, ssh into the running nodes and run top command (top -u userid)
#
# 4
# After the job finishes look at the stdout....txt file
#
# Change the number of tasks in the batch script and see how performance is different
# ----------------------------------------------------------------------------------------

import os
import json
import time
import numpy as np

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' #turn off warning messages
import tensorflow as tf

#-------------------------------------------------
#import horovod.keras as hvd  
import horovod.tensorflow.keras as hvd
hvd.init()
print('INFO, global rank:',hvd.rank(), ' localrank ',hvd.local_rank())
#------------------------------------------------------------

#  On a GPU you would do this:
#      Pin each GPU to a single MPI process. 
gpus_list  = tf.config.experimental.list_physical_devices('GPU')
if gpus_list:
    doGPU=1
    print('INFO,gpus available rank:',hvd.rank(),' ',gpus_list)
    #now pin this MPI rank to single gpu device
    for gpu in gpus_list:
       tf.config.experimental.set_memory_growth(gpu, True)
    tf.config.experimental.set_visible_devices(gpus_list[hvd.local_rank()], 'GPU') #only make this one visible to this rank
else:
    doGPU=0

# On a CPU do this, check out cpu list
cpus_list  = tf.config.experimental.list_physical_devices('CPU')
if cpus_list:
    print('INFO,cpus available rank:',hvd.rank(),' ',cpus_list)
#---------------------------------------------------------------------------

# --- function to get data ----------------
#  This return a numpy data matrix that will be 'sharded' (split among processes)
#  The batch size before sharding is the 'global' batch size (sum of all processes)
# ---------------------------------------------------------------------------
def mnist_dataset_hvd(num_workers,my_rank):
    (X_train, Y_train), (X_test, Y_test) = tf.keras.datasets.mnist.load_data()

    # --------- Reshape input data, b/c Keras expects N-3D images (ie 4D matrix)
    X_train = X_train[:,:,:,np.newaxis]
    X_test  = X_test[:,:,:,np.newaxis]

    if my_rank==0: 
      print('INFO, aft load Xtrain shape',X_train.shape, X_test.shape)
      print('INFO, aft load Ytrain shape',Y_train.shape, Y_test.shape)
    #Scale 0 to 1 
    X_train = X_train/255.0
    X_test  = X_test/255.0

    #for just np arrays, shard by rank
    shard_size   = X_train.shape[0]//num_workers  #This assumes an integer result
    if my_rank==0: 
        print('INFO, the per rank shard size is',shard_size)
    begindex     = int(my_rank*shard_size)
    endindex     = int(begindex+shard_size+1)  #add 1 for numpy range to work
    train_dataset= (X_train[begindex:endindex,],Y_train[begindex:endindex,])
    test_dataset = (X_test[begindex:endindex,],Y_test[begindex:endindex,])
    if my_rank==0: 
      print('INFO, aft split, Xtrain shape',train_dataset[0].shape, test_dataset[0].shape)
      print('INFO, aft split, Ytrain shape',train_dataset[1].shape, test_dataset[1].shape)
    
    return (train_dataset, test_dataset)
#------------ end get dataset -------------------------

# ------------------ Get Dataset ---------------------------
per_worker_batch_size = 32        #Pick factors of 32 (especially for GPU)
num_workers           = hvd.size()
if hvd.rank()==0: 
     print('INFO, num workers',num_workers,' rank:',hvd.rank())
train_dataset, test_dataset = mnist_dataset_hvd(hvd.size(),hvd.rank())  


# ------- function to build CNN model -------------
def build_model():
    model = tf.keras.Sequential([
      tf.keras.layers.InputLayer(input_shape=(28, 28)),
      tf.keras.layers.Reshape(target_shape=(28, 28, 1)),
      #add convolution block
      tf.keras.layers.Conv2D(16, 3, activation='relu'),
      tf.keras.layers.Conv2D(16, 3, activation='relu'),
      tf.keras.layers.MaxPooling2D(pool_size=(2,2),strides=2),

      #add classifier layers
      tf.keras.layers.Flatten(),
      tf.keras.layers.Dense(128, activation='relu'),
      tf.keras.layers.Dense(10)
    ])


    # ------------ for HVD ----------------------------------------
    # wrap the Keras optimizer with Horovod's Distributed Optimizer.
    # https://horovod.readthedocs.io/en/latest/keras.html
    # ----------------------------------------------------------

    #------- Enter the num of processes to scale the learning rate here -------
    optimizer2use  = tf.keras.optimizers.Adam(learning_rate=0.001*num_workers)    
    optimizer2use  = hvd.DistributedOptimizer(optimizer2use) #<<<<<<---------

    # ------------ for HVD ----------------------------------------
    #Specify `experimental_run_tf_function=False` to ensure TensorFlow
    # uses hvd.DistributedOptimizer() to compute gradients.
    # ----------------------------------------------------------
    model.compile(
      loss         =tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
      optimizer    =optimizer2use,
      metrics      =['accuracy'],
      experimental_run_tf_function=False)

    return model
# ------------------- end get model ---------------------------------

# +
#--------------    Build Model -------------- -------------------------
multi_worker_model = build_model()
#-----------------------------------------------------------------------

# Print the summary of the model's network architecture
if hvd.rank() == 0:
    multi_worker_model.summary()
# -

time.sleep(10)  #pause so that you can ssh into the node and run top command

# +
# ------------- The call back functions --------------------------
# Horovod will broadcast initial variable states from rank 0 to all other 
# processes. 
hvd_init_bcast = hvd.callbacks.BroadcastGlobalVariablesCallback(0)

#becareful, early stopping could cause some ranks to finish before others, so don't use this
myES_function = tf.keras.callbacks.EarlyStopping(monitor='val_accuracy', 
                            patience=3,  restore_best_weights=True)
#----------------------------------------------------------------
start_time = time.time()

#Note that the train dataset is a list of data and targets
fit_history=multi_worker_model.fit(train_dataset[0],train_dataset[1], 
                   validation_data=test_dataset,
                   epochs=15, 
                   batch_size=per_worker_batch_size, 
                   verbose=2 if hvd.rank() == 0 else 0,
                   callbacks=[hvd_init_bcast] 
                   )

training_time = time.time() - start_time
print('INFO,done, rank: ',hvd.rank(),' train time:',np.round(training_time,5),' secs')

if hvd.rank()==0:
  valhistory=fit_history.history['val_accuracy']
  print('INFO, min val acc=',min(valhistory), ' indx:',np.argmax(valhistory) )
  #print(valhistory)
# -

# check rank to ensure only rank 0 does model checkpoints, model saves, or evaluation
if hvd.rank() == 0:
   print('INFO, This is rank 0 instance model evaluation')
   print(multi_worker_model.evaluate(test_dataset[0],test_dataset[1]))

#also, another potential useful function to use on GPUs
# Returns a dict in the form {'current': <current mem usage>,
#                             'peak': <peak mem usage>}
if doGPU:
  print('Info, Mem for gpu for rank:',hvd.rank(),tf.config.experimental.get_memory_info('GPU:0'))
