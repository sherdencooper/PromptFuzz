#!/bin/bash

PYTHON_SCRIPT="./Experiment/run.py"
PHASE="init"
MODE="hijacking"
NO_MUTATE="True"

# Set the log path
LOG_PATH="Logs/${PHASE}/${MODE}"

# Create the log directory if it does not exist
mkdir -p "$LOG_PATH"

# Function to run the Python script
run_python_script() {
    local index=$1
    python -u "$PYTHON_SCRIPT" --index $index --phase $PHASE --mode $MODE --no_mutate $NO_MUTATE > "${LOG_PATH}/${index}.log" 2>&1
    echo "Task $index finished."
}

# Start the jobs with a limit of 2 tasks in parallel
for index in {0..10}; do
    run_python_script $index &
    ((index++))
    [ $((index % 2)) -eq 0 ] && wait
done

# Wait for all background jobs to finish
wait
