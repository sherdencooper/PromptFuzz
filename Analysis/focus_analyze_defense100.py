import csv
import os
import json
import ast
    
    
    

if __name__ == '__main__':
    csv_dir = '../Results/focus/extraction/finetuned1_single_3'
    log_dir = '../Logs/focus/extraction/finetuned1_token_3'
    defense_path = '../Datasets/extraction_focus_seed.jsonl'
    file_list = os.listdir(csv_dir)
    all_results = list()
    with open(defense_path) as f:
        lines = f.readlines()
    defenses = [json.loads(line) for line in lines] 
    for csv_file in file_list:
        index = csv_file.split('.')[0]
        csv_path = os.path.join(csv_dir,csv_file)
        with open(csv_path) as f:
            reader = csv.reader(f)
            rows = list(reader)
            if len(rows) == 1:
                row = ['']*8
            else:
                row = rows[1]
                parent = int(row[-4])
                parent_prompt = defenses[parent]['attack']
                row.append(parent_prompt)
            row.insert(0,index)
            #all_results.append(row)
            log_path = os.path.join(log_dir,f"defense_{index}.log")
            print(log_path)
            with open(log_path) as f:
                lines = f.readlines()
            token_counts = 0
            for line in lines:
                try:
                    token_dict = json.loads(line.strip()[12:])
                except Exception as e:
                    print(line)
                token_counts += token_dict['total_tokens']
            row.append(token_counts)
            all_results.append(row)
    with open('../Analyze_results/finetuned1_focus_attack_result_defense100_3.csv','w') as f:
        writer = csv.writer(f)
        writer.writerow(['defense_index','index','prompt','response','parent','results','mutation','query','parent_prompt','total_tokens'])
        for result in all_results:
            writer.writerow(result)
