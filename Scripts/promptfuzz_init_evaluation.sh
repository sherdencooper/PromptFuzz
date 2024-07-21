#!/bin/bash

PYTHON_SCRIPT="./Experiment/run.py"
PHASE="init"
MODE="hijacking"
NO_MUTATE="True"


# Check if NO_MUTATE should be set to true
NO_MUTATE_FLAG=""

if [ "$NO_MUTATE" = "True" ]; then
  NO_MUTATE_FLAG="--no_mutate"
fi

# Set the log path
LOG_PATH="Logs/${PHASE}/${MODE}"

# Create the log directory if it does not exist
mkdir -p "$LOG_PATH"

# Function to run the Python script
run_python_script() {
    local index=$1
    python -u "$PYTHON_SCRIPT" --index $index --phase $PHASE --mode $MODE $NO_MUTATE_FLAG > "${LOG_PATH}/${index}.log" 2>&1
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
