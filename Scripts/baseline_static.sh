#!/bin/bash

PYTHON_SCRIPT="./Experiment/run.py"
PHASE="init"
MODE="hijacking"
NO_MUTATE="True"
ALL_DEFENSES="False"

FEW_SHOT="False"
DYNAMIC_ALLOCATE="False"
MAX_JAILBREAK=1

BASELINE="initial_seed" # human_expert, gcg, initial_seed

# Check if NO_MUTATE, ALL_DEFENSES, FEW_SHOT, and DYNAMIC_ALLOCATE should be set to true
NO_MUTATE_FLAG=""
ALL_DEFENSES_FLAG=""
FEW_SHOT_FLAG=""
DYNAMIC_ALLOCATE_FLAG=""

if [ "$NO_MUTATE" = "True" ]; then
  NO_MUTATE_FLAG="--no_mutate"
fi

if [ "$ALL_DEFENSES" = "True" ]; then
  ALL_DEFENSES_FLAG="--all_defenses"
fi

if [ "$FEW_SHOT" = "True" ]; then
  FEW_SHOT_FLAG="--few_shot"
fi

if [ "$DYNAMIC_ALLOCATE" = "True" ]; then
  DYNAMIC_ALLOCATE_FLAG="--dynamic_allocate"
fi


# Set the log path
LOG_PATH="Logs/${PHASE}/${MODE}/baseline/${BASELINE}/"

# Create the log directory if it does not exist
mkdir -p "$LOG_PATH"

# Function to run the Python script
run_python_script() {
    local index=$1
    # python -u "$PYTHON_SCRIPT" --index $index --phase $PHASE --mode $MODE $NO_MUTATE_FLAG > "${LOG_PATH}/${index}.log" 2>&1
    python -u "$PYTHON_SCRIPT" --index $index --max_jailbreak $MAX_JAILBREAK \
        --phase $PHASE --mode $MODE $NO_MUTATE_FLAG $ALL_DEFENSES_FLAG $FEW_SHOT_FLAG $DYNAMIC_ALLOCATE_FLAG \
        --baseline $BASELINE > "${LOG_PATH}/${index}.log" 2>&1
    echo "Task $index finished."
}

# Run the Python script
for index in {0..150}; do
    run_python_script $index &
    ((index++))
    [ $((index % 32)) -eq 0 ] && wait
done

echo "All tasks finished."