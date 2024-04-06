#!/bin/bash

PYTHON_SCRIPT="./Experiment/run.py"
PHASE="focus"
MODE="extraction"
NO_MUTATE="False"
ALL_DEFENSES="True"
RETRIEVAL_METHOD="cosine_similarity"
CLUSTER_NUM=5
THRESHOLD_COEFFICIENT=0.5
FEW_SHOT="True"
DYNAMIC_ALLOCATE="True"
FEW_SHOT_NUM=3

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
LOG_PATH="Logs/${PHASE}/${MODE}/${RETRIEVAL_METHOD}"

# Create the log directory if it does not exist
mkdir -p "$LOG_PATH"

# Run the Python script
python -u "$PYTHON_SCRIPT" --phase $PHASE --mode $MODE $NO_MUTATE_FLAG $ALL_DEFENSES_FLAG $FEW_SHOT_FLAG $DYNAMIC_ALLOCATE_FLAG --retrieval_method $RETRIEVAL_METHOD --cluster_num $CLUSTER_NUM --threshold_coefficient $THRESHOLD_COEFFICIENT --few_shot_num $FEW_SHOT_NUM > "${LOG_PATH}/all_defenses.log" 2>&1

echo "All tasks finished."
