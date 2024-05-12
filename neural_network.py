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
from keras import backend as K
from keras import layers
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# Plotting Function
def plot_training_history(history):
    # Plot training & validation accuracy values
    plt.plot(history.history['accuracy'])
    plt.plot(history.history['val_accuracy'])
    plt.title('Model accuracy')
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Validation'], loc='upper left')
    plt.show()

    # Plot training & validation loss values
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('Model loss')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Validation'], loc='upper left')
    plt.show()

# Precision/F1 Functions
def recall_m(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    recall = true_positives / (possible_positives + K.epsilon())
    return recall

def precision_m(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    return precision

def f1_m(y_true, y_pred):
    precision = precision_m(y_true, y_pred)
    recall = recall_m(y_true, y_pred)
    return 2*((precision*recall)/(precision+recall+K.epsilon()))

# Program Launch
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

# Load Dataset
dataset = pd.read_csv(dataset_path)
num_columns = dataset.shape[1]

# Remove Incomplete Rows
incomplete_rows_before = dataset.isnull().sum().sum()
print(f"Found {incomplete_rows_before} incomplete rows... Removing")
dataset = dataset.dropna()

# Exit if invalid rows remain
incomplete_rows_after = dataset.isnull().sum().sum() == 0
if (incomplete_rows_after == 0):
    print(f"{incomplete_rows_after}Invald entries remaining in dataset, Aborting...")
    sys.exit(0)

# Split Dataset
X = dataset.drop(['survived', 'name'], axis=1)  # Input features
y = dataset['survived']                         # Target variable


num_inputs = X.shape[1] # For survival and name
print(f"Number of inputs = {num_inputs}")

X_train, X_val, y_train, y_val = train_test_split(X, y, train_size=split, random_state=34)
X_val, X_test, y_val, y_test = train_test_split(X_val, y_val, train_size=split/2, random_state=34)

# Define Model
# RLEU activation + Sigmoid Output
# l2 Regulaizer
sequential_model = keras.Sequential(
    [
        layers.Input(shape=(num_inputs,)),
        layers.Dense(32,    activation="elu",   kernel_regularizer=keras.regularizers.l2(0.001)),
        layers.Dense(64,    activation="elu",   kernel_regularizer=keras.regularizers.l2(0.001)),
        layers.Dense(128,   activation="elu",   kernel_regularizer=keras.regularizers.l2(0.001)),
        layers.Dense(64,    activation="elu",   kernel_regularizer=keras.regularizers.l2(0.001)),
        layers.Dense(32,    activation="elu",   kernel_regularizer=keras.regularizers.l2(0.001)),
        layers.Dense(1,     activation='sigmoid')
    ]
)

# Compile Model
sequential_model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy', f1_m, precision_m, recall_m]
)

# Train Model
checkpoint = keras.callbacks.ModelCheckpoint(
    f"./models/{file[:-4]}.hdf5", 
    monitor='val_accuracy', 
    verbose=1, 
    save_best_only=True, 
    mode='auto', 
    period=1, 
    save_weights_only=False
)

# Train
history = sequential_model.fit(
    X_train, 
    y_train, 
    epochs=train_epochs, 
    validation_data=(X_val, y_val), 
    callbacks=[checkpoint]
)

# Access metrics from the callback
print("Best Validation Accuracy:", checkpoint.best)

sequential_model.evaluate(
    x=X_test,
    y=y_test,
    verbose="auto",
    sample_weight=None,
    steps=None,
    callbacks=checkpoint,
    return_dict=False,
)

# Plot
plot_training_history(history)

# Save Model
outputPath = f"./models/{file[:-4]}.keras"
try:
    sequential_model.save(outputPath)
except:
    print(f"Error saving model: {outputPath} is invalid")
    sys.exit(1)    
print(f"Model Saved to {outputPath}")
sys.exit(0)
