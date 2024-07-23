#!/bin/bash

GET_METRICS_SCRIPT="./Experiment/get_metric.py"

METHOD="promptfuzz"
TARGET_FILE=""
SAVE_FILE=""
AGGREGATE_CSV_FILE_PATH=""
DEFENSE_NUM=150

# Run the Python script
python -u "$GET_METRICS_SCRIPT" --target_file $TARGET_FILE --save_file $SAVE_FILE --aggregate_csv_file_path $AGGREGATE_CSV_FILE_PATH --defense_num $DEFENSE_NUM
echo "Get metrics finished."