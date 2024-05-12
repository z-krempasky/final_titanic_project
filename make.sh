#!/bin/bash

# Get the directory of the script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Define the models folder
MODELS_FOLDER="$SCRIPT_DIR/models"

# Define the arguments for the crew target
CREW_ARGS="crew_dataset.csv 0.6 100"

# Define the arguments for the passenger target
PASSENGER_ARGS="passenger_dataset.csv 0.6 100"

crew() {
    # Run the Python script
    python "neural_network.py" $CREW_ARGS
}

passenger() {
    # Run the Python script with passenger arguments
    python "neural_network.py" $PASSENGER_ARGS
}

all() {
    # Run both crew and passenger
    crew
    passenger
}

clean() {
    # Clear the contents of the models folder
    rm -rf "$MODELS_FOLDER"/*.keras
    rm -rf "$MODELS_FOLDER"/*.hdf5
}

# Parse command-line arguments
case "$1" in
    crew)
        crew
        ;;
    passenger)
        passenger
        ;;
    all)
        all
        ;;
    clean)
        clean
        ;;
    *)
        echo "Usage: $0 {crew|passenger|all|clean}"
        exit 1
esac

exit 0
