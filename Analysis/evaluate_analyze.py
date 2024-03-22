import csv
import os
import json
import ast

def analyze(csv_path,attack_id_num,total_attack,attack_seed_path):
    with open(attack_seed_path,'r') as f:
        data = [json.loads(line) for line in f.readlines()]
 
    attack_success_dict = dict()
    for attack_id in range(attack_id_num):
        attack_success_dict[attack_id] = 0
    with open(csv_path) as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == 'index':
                continue 
            attack_id = int(row[-4])
            attack_results = ast.literal_eval(row[-3])
            success_attack = sum(attack_results)
            attack_success_dict[attack_id] += success_attack
    
    attack_result = list()
    for attack_id in attack_success_dict.keys():
        success_attack = attack_success_dict[attack_id]
        sample_id = data[attack_id]['sample_id']
        attack_result.append([attack_id,round(success_attack/total_attack,3),sample_id])
    attack_result.sort(key=lambda x:x[1],reverse=True)
    
    
    with open('../Analyze_results/evaluate_attack_result.csv','w') as f:
        writer = csv.writer(f)
        writer.writerow(['AttackID','AttackSuccessRate','SampleID'])
        for result in attack_result:
            writer.writerow(result)
    # get focus seeds
    focus_seeds = []
    for i in range(40):
        attack_id = attack_result[i][0]
        focus_seeds.append(data[attack_id])
    save_filename = 'extraction_focus_seed.jsonl'
    save_path = os.path.join('../Datasets',save_filename)
    with open(save_path,'w') as f:
        for item in focus_seeds:
            line = json.dumps(item)
            f.write(line+'\n')
    mutator_dict = dict()
    with open(csv_path) as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == 'index':
                continue
            attack_id = int(row[3])
            attack = data[attack_id]['attack']
            sample_id = data[attack_id]['sample_id']
            row.append(attack)
            row.append(sample_id)
            mutator = row[-4]
            seed_list = mutator_dict.get(mutator,list())
            seed_list.append(row)
            mutator_dict[mutator] = seed_list
    mutator_examples = []
    for mutator in mutator_dict.keys():
        seed_list = mutator_dict[mutator]
        if len(seed_list) < 20:
            mutator_examples += seed_list[:len(seed_list)]
        else:
            mutator_examples += seed_list[:20]
    save_filename = 'extraction_evaluate_example.csv'
    save_path = os.path.join('../Datasets',save_filename)
    with open(save_path,'w') as f:
        writer = csv.writer(f)
        writer.writerow(
            ['index', 'prompt', 'response', 'parent', 'results', 'mutation', 'query','parent_prompt','parent_sample_id'])
        for example in mutator_examples:
            writer.writerow(example)
         
        
    

if __name__ == '__main__':
    csv_path = '../Results/evaluate/extraction/all_results.csv'
    attack_seed_path = '../Datasets/extraction_evaluate_seed.jsonl'
    attack_id_num = 81
    total_attack = 10*50
    analyze(csv_path,attack_id_num,total_attack,attack_seed_path)
