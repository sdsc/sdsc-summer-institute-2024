# ----------------------------------------------------
#  MNIST with the 'mirror strategy' code added
# ---------------------------------------------------

import os
import json
import time
import numpy as np

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' 
import tensorflow as tf

gpus_list  = tf.config.experimental.list_physical_devices('GPU')
print('INFO,gpus available ',gpus_list)
n_gpus     = len(gpus_list)
print("INFO,config,Num GPUs:", n_gpus)

for gpu in gpus_list:
    tf.config.experimental.set_memory_growth(gpu, True)  
#----------------------------------------------------------------------------

#  Check out cpu list
cpus_list  = tf.config.experimental.list_physical_devices('CPU')
print('INFO,cpus available ',cpus_list)
#---------------------------------------------------------------------------



# --- function to get data ----------------
#  This return a tensorflow dataset that will be 'sharded' (split among processes)
#  The batch size before sharding is the 'global' batch size (sum of all processes)
#  and if this runs on 1 device then it would also be the local batch size
# ---------------------------------------------------------------------------
def mnist_dataset_hvd(b4shard_batch_size):
    (X_train, Y_train), (X_test, Y_test) = tf.keras.datasets.mnist.load_data()

    # --------- Reshape input data, b/c Keras expects N-3D images (ie 4D matrix)
    X_train = X_train[:,:,:,np.newaxis]
    X_test  = X_test[:,:,:,np.newaxis]

    print('INFO, aft load Xtrain shape',X_train.shape, X_test.shape)
    print('INFO, aft load Ytrain shape',Y_train.shape, Y_test.shape)
    #Scale 0 to 1 
    X_train = X_train/255.0
    X_test  = X_test/255.0

    train_dataset = tf.data.Dataset.from_tensor_slices((X_train, Y_train)).shuffle(60000).batch(b4shard_batch_size)
    test_dataset  = tf.data.Dataset.from_tensor_slices((X_test, Y_test)).shuffle(10000).batch(b4shard_batch_size)

    return (train_dataset,test_dataset)
#------------ end get dataset -------------------------

# ------- function build model -------------
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


    optimizer2use  = tf.keras.optimizers.Adam(learning_rate=0.001)

    model.compile(
      loss         =tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
      optimizer    =optimizer2use,
      metrics      =['accuracy'])
    # experimental_run_tf_function=False)

    return model
# ------------------- end get model ---------------------------------



per_worker_batch_size = 32

# ------------------ Get Dataset ---------------------------
#get data as a tensorflow dataset and shard it (so each worker gets a part)
#------------------------------------
train_dataset, test_dataset = mnist_dataset_hvd(per_worker_batch_size*4)  
if 0: #use this if its a tensorflow dataset object
  for element in train_dataset.as_numpy_iterator():
    print('INFO, after shard, element check y-elem:',element[1])
    break

#------------------------------------------------------------

#---------------------------------------------------------
#   Set up strategy 
#----------------------------------------------------------
#mirrored_strategy = tf.distribute.MirroredStrategy(["GPU:0", "GPU:1",  "GPU:2",  "GPU:3"])
if (n_gpus>0):
    mirrored_strategy = tf.distribute.MirroredStrategy(["GPU:0", "GPU:1",  "GPU:2",  "GPU:3"])
    with mirrored_strategy.scope():
      multi_dev_model=build_model()  
else:
    print('INFO.. no gpus available, using CPU:0')
    #exit()
    mirrored_strategy = tf.distribute.MirroredStrategy(["CPU:0"])
    with mirrored_strategy.scope():
      multi_dev_model=build_model()  
#---------------------------------------------------------


multi_dev_model.summary()

myES_function = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=5,  restore_best_weights=True)

#multi_dev_model.fit(train_dataset[0],train_dataset[1],  use this for numpy arrays in train dataset tuple

time.sleep(120)  #wait 2 min to use nvidia-smi or top command to check out gpu or cpu usage

multi_dev_model.fit(train_dataset, 
                   validation_data=test_dataset,
                   epochs=5, 
                   batch_size=per_worker_batch_size, 
                   verbose=2,
                   callbacks=[myES_function],  
                    )
print('INFO, done')




