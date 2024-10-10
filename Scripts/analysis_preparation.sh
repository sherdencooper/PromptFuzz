#!/bin/bash

MODE="hijacking" # extraction
GET_ATTACK_RANKING_SCRIPT="./Experiment/sample_topN_focus_seed.py"
SAMPLE_EXAMPLE_BY_MUTATOR_SCRIPT="./Experiment/sample_example_by_mutator.py"
GET_MUTATOR_WEIGHTS_SCRIPT="./Experiment/get_mutator_weights.py"

TARGET_FILE="./Results/preparation/${MODE}/all_results.csv"
INIT_FILE="./Datasets/${MODE}_preparation_seed.jsonl"

OUTPUT_FILE_SEED="./Datasets/${MODE}_focus_seed.jsonl"
OUTPUT_FILE_EXAMPLE="./Datasets/${MODE}_few_shot_example.csv"
OUTPUT_FILE_EXAMPLE_MUTATOR="./Results/preparation/${MODE}/mutator_weights.csv"

# Run the Python script
python -u "$GET_ATTACK_RANKING_SCRIPT" --target_file $TARGET_FILE --init_file $INIT_FILE --output_file $OUTPUT_FILE_SEED 
echo "Sampled top N focus seed tasks finished."

python -u "$SAMPLE_EXAMPLE_BY_MUTATOR_SCRIPT" --target_file $TARGET_FILE --init_file $INIT_FILE --output_file $OUTPUT_FILE_EXAMPLE
echo "Sampled few-shot example tasks finished."

python -u "$GET_MUTATOR_WEIGHTS_SCRIPT" --target_file $TARGET_FILE --output_file $OUTPUT_FILE_EXAMPLE_MUTATOR
echo "Get mutator weights finished."
