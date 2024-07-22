#!/bin/bash

GET_ATTACK_RANKING_SCRIPT="./Experiment/sample_topN_focus_seed.py"
SAMPLE_EXAMPLE_BY_MUTATOR_SCRIPT="./Experiment/sample_example_by_mutator.py"

TARGET_FILE=""
INIT_FILE="./Datasets/hijacking_preparation_seed.jsonl"

OUTPUT_FILE_SEED="./Datasets/hijacking_focus_seed.jsonl"
OUTPUT_FILE_EXAMPLE="./Datasets/hijacking_focus_example.jsonl"

# Run the Python script
python -u "$GET_ATTACK_RANKING_SCRIPT" --target_file $TARGET_FILE --init_file $INIT_FILE --output_file $OUTPUT_FILE_SEED 
echo "Sampled top N focus seed tasks finished."

python -u "$SAMPLE_EXAMPLE_BY_MUTATOR_SCRIPT" --target_file $TARGET_FILE --init_file $INIT_FILE --output_file $OUTPUT_FILE_EXAMPLE
echo "Sampled few-shot example tasks finished."
