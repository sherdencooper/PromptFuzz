#!/bin/bash

PYTHON_SCRIPT="./Experiment/run.py"
PHASE="evaluate"
MODE="hijacking"
NO_MUTATE="False"
ALL_DEFENSES="True"

# Check if NO_MUTATE and ALL_DEFENSES should be set to true
NO_MUTATE_FLAG=""
ALL_DEFENSES_FLAG=""

if [ "$NO_MUTATE" = "True" ]; then
  NO_MUTATE_FLAG="--no_mutate"
fi

if [ "$ALL_DEFENSES" = "True" ]; then
  ALL_DEFENSES_FLAG="--all_defenses"
fi

# Set the log path
LOG_PATH="Logs/${PHASE}/${MODE}"

# Create the log directory if it does not exist
mkdir -p "$LOG_PATH"

# Run the Python script
python -u "$PYTHON_SCRIPT" --phase $PHASE --mode $MODE $NO_MUTATE_FLAG $ALL_DEFENSES_FLAG > "${LOG_PATH}/all_defenses.log" 2>&1

echo "All tasks finished."

