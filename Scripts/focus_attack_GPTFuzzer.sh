#!/bin/bash

PYTHON_SCRIPT="./Experiment/run.py"
PHASE="focus"
MODE="extraction"
NO_MUTATE="False"
ALL_DEFENSES="True"
RETRIEVAL_METHOD="random"
CLUSTER_NUM=5
THRESHOLD_COEFFICIENT=0.5
FEW_SHOT="False"
DYNAMIC_ALLOCATE="False"
FEW_SHOT_NUM=3
#FEW_SHOT_NUM=$1
#MODEL_PATH="ft:gpt-3.5-turbo-0125:northwestern-university::9LTrBZ8O"
MODEL_PATH="gpt-3.5-turbo-0125"

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
LOG_PATH="Logs/${PHASE}/${MODE}/"
# Create the log directory if it does not exist
mkdir -p "$LOG_PATH"

# Run the Python script
python -u "$PYTHON_SCRIPT" --phase $PHASE --mode $MODE --model_path $MODEL_PATH $NO_MUTATE_FLAG $ALL_DEFENSES_FLAG $FEW_SHOT_FLAG $DYNAMIC_ALLOCATE_FLAG --retrieval_method $RETRIEVAL_METHOD --cluster_num $CLUSTER_NUM --threshold_coefficient $THRESHOLD_COEFFICIENT --few_shot_num $FEW_SHOT_NUM > "${LOG_PATH}/all_defenses_GPTFuzzer.log" 2>&1

echo "All tasks finished."
