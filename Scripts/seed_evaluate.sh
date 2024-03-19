#!/bin/bash

PYTHON_SCRIPT="./Experiment/run.py"
PHASE="evaluate"
MODE="hijacking"
NO_MUTATE="False"
ALL_DEFENSES="True"

# Set the log path
LOG_PATH="Logs/${PHASE}/${MODE}"

# Create the log directory if it does not exist
mkdir -p "$LOG_PATH"

# Run the Python script
python -u "$PYTHON_SCRIPT" --phase $PHASE --mode $MODE --no_mutate $NO_MUTATE --all_defenses $ALL_DEFENSES > "${LOG_PATH}/all_defenses.log" 2>&1

echo "All tasks finished."
