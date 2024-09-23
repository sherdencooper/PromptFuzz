#!/bin/bash

PYTHON_SCRIPT="./Experiment/run.py"
PHASE="focus"
MODE="hijacking"
NO_MUTATE="False"
ALL_DEFENSES="False"
RETRIEVAL_METHOD="cosine_similarity"
CLUSTER_NUM=5
THRESHOLD_COEFFICIENT=0.5
FEW_SHOT="True"
DYNAMIC_ALLOCATE="True"
FEW_SHOT_NUM=3
INDEX=0
MAX_JAILBREAK=1
MUTATOR_WEIGHTS_HIJACKING=(0.21 0.23 0.13 0.23 0.2)
MUTATOR_WEIGHTS_EXTRATION=(0.1 0.1 0.4 0.2 0.2)
IS_FINETUNED="True"
FINE_TUNE_MODEL_PATH=""

# Check if NO_MUTATE, ALL_DEFENSES, FEW_SHOT, and DYNAMIC_ALLOCATE should be set to true
NO_MUTATE_FLAG=""
ALL_DEFENSES_FLAG=""
FEW_SHOT_FLAG=""
DYNAMIC_ALLOCATE_FLAG=""
MUTATOR_WEIGHTS=""
MODEL_PATH=""


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

if [ "$MODE" = "hijacking" ]; then
  MUTATOR_WEIGHTS=${MUTATOR_WEIGHTS_HIJACKING[@]}
else
  MUTATOR_WEIGHTS=${MUTATOR_WEIGHTS_EXTRATION[@]}
fi

if [ "$IS_FINETUNED" = "True" ]; then
  MODEL_PATH="--model_path $FINE_TUNE_MODEL_PATH"
fi

# Set the log path
if [ "$IS_FINETUNED" = "True" ]; then
    LOG_PATH="Logs/${PHASE}/${MODE}/challenging_defenses_finetuned/"
else
    LOG_PATH="Logs/${PHASE}/${MODE}/challenging_defenses_basemodel/"
fi

# Create the log directory if it does not exist
mkdir -p "$LOG_PATH"

# Function to run the Python script
run_python_script() {
    local index=$1
    # python -u "$PYTHON_SCRIPT" --index $index --phase $PHASE --mode $MODE $NO_MUTATE_FLAG > "${LOG_PATH}/${index}.log" 2>&1
    python -u "$PYTHON_SCRIPT" --index $index \
        --phase $PHASE \
        --mode $MODE \
        $MODEL_PATH \
        --max_jailbreak $MAX_JAILBREAK \
        $NO_MUTATE_FLAG \
        $ALL_DEFENSES_FLAG \
        $FEW_SHOT_FLAG \
        --retrieval_method $RETRIEVAL_METHOD \
        --cluster_num $CLUSTER_NUM \
        --few_shot_num $FEW_SHOT_NUM
        $DYNAMIC_ALLOCATE_FLAG \
        --threshold_coefficient $THRESHOLD_COEFFICIENT \
        --mutator_weights $MUTATOR_WEIGHTS> "${LOG_PATH}/${index}.log" 2>&1
    echo "Task $index finished."
}

# Run the Python script
for index in {0..29}; do
    run_python_script $index &
    ((index++))
    [ $((index % 8)) -eq 0 ] && wait
done
# run_python_script 28

echo "All tasks finished."
