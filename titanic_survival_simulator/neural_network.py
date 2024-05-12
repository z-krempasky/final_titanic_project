##################################################################
# neural_network.py - By Ryan Massie
# Defines functions for congfiguring, training, testing, saving, 
# loading, and executing, neural networks
#
##################################################################
# Libraries
import sys
import os
import pandas as pd
import tensorflow as tf
import keras
from keras import layers
from sklearn.model_selection import train_test_split
# Functions
# Convert X, y data frames to train/test tensors
def tensorize(X, y, size, split):
    X_tensor = tf.convert_to_tensor(X.values, dtype=tf.float32)
    y_tensor = tf.convert_to_tensor(y.values.reshape(-1, 1), dtype=tf.float32)  # Reshape y to have shape [num_samples, 1]

    # Ensure that the shapes match, then combine
    assert X_tensor.shape[0] == y_tensor.shape[0], "Number of samples in X and y must match"
    combined_tensor = tf.concat([X_tensor, y_tensor], axis=1)

    # Shuffle the combined tensor
    shuffled_tensor = tf.random.shuffle(combined_tensor)
    # Split the shuffled tensor into X_train, X_test, y_train, and y_test
    num_train_samples = int(split * size)
    X_train = shuffled_tensor[:num_train_samples, :-1]  # Input features for training
    y_train = shuffled_tensor[:num_train_samples, -1:]  # Output labels for training
    X_test = shuffled_tensor[num_train_samples:, :-1]   # Input features for testing
    y_test = shuffled_tensor[num_train_samples:, -1:]   # Output labels for testing
    return X_train, X_test, y_train, y_test

# Program Execution
expected_args_count = 3
script_name = sys.argv[0]

# Argv validation
if len(sys.argv) != (expected_args_count + 1):  # Adding 1 for the script name
    print(f"Incorrect args {len(sys.argv)}- usage: python {script_name} <dataset> <train%> <epochs>")
    sys.exit(1)

file = sys.argv[1]
dataset_path = "./datasets/" + file
if not os.path.exists(dataset_path):
    print(f"Invalid path to dataset - {dataset_path}")
    sys.exit(1)

try:
    split = float(sys.argv[2])
    if not (0 < split <= 100):
        raise ValueError
except ValueError:
    print(f"Error: Argument {sys.argv[2]} is not a valid percentage greater than 0.")
    sys.exit(1)

try:
    train_epochs = int(sys.argv[3])
    if not (0 < train_epochs):
        raise ValueError
except ValueError:
    print(f"Error: Argument {sys.argv[3]} is not a valid epoch number (greater than 0).")
    sys.exit(1)

# Confirm Output Directory
model_output = "./models/"

# Load Dataset
dataset = pd.read_csv(dataset_path)
num_columns = dataset.shape[1]
num_inputs = num_columns - 2 # For survival and name

# Create Datasets
X = dataset.drop(['survived', 'name'], axis=1)  # Input features
y = dataset['survived']                         # Target variable
X_train, X_test, y_train, y_test = tensorize(X, y, num_columns, split)

# Define Model
# Input --> 16 --> 32 --> 64 --> 32 --> 16 --> 1
# RLEU activation + Sigmoid Output
sequential_model = keras.Sequential(
    [
        layers.Input(shape=(num_inputs,),           name="layer_input"  ),
        layers.Dense(16,    activation="relu",      name="layer1"       ),
        layers.Dense(32,    activation="relu",      name="layer2"       ),
        layers.Dense(64,    activation="relu",      name="layer3"       ),
        layers.Dense(32,    activation="relu",      name="layer6"       ),
        layers.Dense(16,    activation="relu",      name="layer7"       ),
        layers.Dense(1,     activation='sigmoid',   name="layer_output" )
    ]
)

sequential_model.compile(
    optimizer="rmsprop",
    loss=keras.losses.BinaryCrossentropy(from_logits=True),
    loss_weights=None,
    metrics=None,
    weighted_metrics=None,
    run_eagerly=False,
    steps_per_execution=1,
    jit_compile="auto",
    auto_scale_loss=True,
)

# Train Model
checkpoint = keras.callbacks.ModelCheckpoint(
    "./models/checpoint.hdf5", 
    monitor = 'val_accuracy', 
    verbose=2, 
    save_best_only=True, 
    mode='auto', 
    period=1, 
    save_weights_only=False
)

# Train
sequential_model.fit(
    X_train, 
    y_train, 
    epochs=train_epochs, 
    validation_data=(X_test, y_test), 
    callbacks=[checkpoint]
)

# Save
outputPath = f"./models/{file[:-4]}.keras"
try:
    sequential_model.save(outputPath)
except:
    print(f"Error saving model: {outputPath} is invalid")
    sys.exit(1)    
print(f"Model Saved to {outputPath}")
sys.exit(0)
