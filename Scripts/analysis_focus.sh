#!/bin/bash

GET_METRICS_SCRIPT="./Experiment/get_metric.py"

METHOD="gcg" # human_expert, gcg, gptfuzz, initial_seed
MODE="hijacking"
if [ "$METHOD" = "gcg" ] || [ "$METHOD" = "human_expert" ] || [ "$METHOD" = "initial_seed" ]; then
    TARGET_PATH="./Results/init/${MODE}/baseline/${METHOD}/"
    SAVE_PATH="./Results/init/${MODE}/baseline/${METHOD}_metrics.csv"        
elif [ "$METHOD" = "gptfuzz" ]; then
    TARGET_PATH="./Results/focus/${MODE}/baseline/all_results.csv"
    SAVE_PATH="./Results/focus/${MODE}/baseline/metrics.csv"
else
    TARGET_PATH="./Results/focus/${MODE}/all_results.csv"
    SAVE_PATH="./Results/focus/${MODE}/metrics.csv"
fi

AGGREGATE_CSV_FILE_PATH="./Results/init/${MODE}/baseline/${METHOD}_aggregate.csv"
DEFENSE_NUM=150

# Run the Python script
python -u "$GET_METRICS_SCRIPT" --method $METHOD \
    --target_path $TARGET_PATH \
    --save_path $SAVE_PATH \
    --aggregate_csv_file_path $AGGREGATE_CSV_FILE_PATH \
    --defense_num $DEFENSE_NUM
echo "Get metrics finished."