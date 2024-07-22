import json
import pandas as pd

# Read the csv file
df = pd.read_csv('Results/evaluate/hijacking/hijacking_focus_defense_rate100.csv')
sample_id = df['sample_id'].to_list()

# Read the jsonl file
with open('Datasets/hijacking_focus_defense.jsonl', 'r') as f:
    defenses = [json.loads(line) for line in f.readlines()]

# Get the focus defenses
focus_defenses = []
for sample in defenses:
    if sample['sample_id'] in sample_id:
        focus_defenses.append(sample)

# Write the focus defenses to a new jsonl file
with open('Datasets/hijacking_focus_defense_rate100.jsonl', 'w') as f:
    for defense in focus_defenses:
        f.write(json.dumps(defense) + '\n')
