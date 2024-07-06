import json
import csv






if __name__ == "__main__":
    focus_defense = '../Datasets/extraction_focus_defense.jsonl'
    focus_dataset_result = '../Analyze_results/focus_dataset_result.csv'
    with open(focus_defense) as f:
        lines = f.readlines()
    index_map = dict()
    for i,line in enumerate(lines):
        sampleID =  str(json.loads(line)['sample_id'])
        index_map[sampleID] = i
    defense100_index = []
    with open(focus_dataset_result) as f:
        csv_reader = csv.reader(f)
        for row in csv_reader:
            if row[0] == 'DefenseID':
                continue
            if float(row[1]) < 1:
                continue
            sampleID = row[2]
            defense100_index.append(index_map[sampleID])
    print(defense100_index)
        

