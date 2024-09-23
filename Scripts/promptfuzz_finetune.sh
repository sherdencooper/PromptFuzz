#!/bin/bash

PYTHON_SCRIPT="./Finetune/fine_tune.py"
API_KEY=''
PHASE="finetuned"
WORK_STAGE="start"
FINE_TUNE_JOB_ID=""

# Set the log path
LOG_PATH="Logs/${PHASE}/${WORK_STAGE}/"

# Create the log directory if it does not exist
mkdir -p "$LOG_PATH"

if [ "$WORK_STAGE" = "start" ]; then    
    python -u "$PYTHON_SCRIPT" --work_stage $WORK_STAGE --api_key $API_KEY > "${LOG_PATH}/fine_tune.log" 2>&1
else
    if [ -z "$FINE_TUNE_JOB_ID" ]; then
        echo "Please provide the fine-tune job ID."
        exit 1
    fi
    python -u "$PYTHON_SCRIPT" --work_stage $WORK_STAGE --api_key $API_KEY --fine_tune_job_id $FINE_TUNE_JOB_ID> "${LOG_PATH}/fine_tune.log" 2>&1
fi

echo "${WORK_STAGE} Finished."