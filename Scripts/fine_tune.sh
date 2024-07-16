#!/bin/bash

PYTHON_SCRIPT="./Experiment/fine_tune.py"
PHASE="finetuned"
WORK_STAGE="check"

# Set the log path
LOG_PATH="Logs/${PHASE}"

# Create the log directory if it does not exist
mkdir -p "$LOG_PATH"

python -u "$PYTHON_SCRIPT" --work_stage $WORK_STAGE > "Logs/${PHASE}/fine_tune.log" 2>&1

echo "${WORK_STAGE} Finished."