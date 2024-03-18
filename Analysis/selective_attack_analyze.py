import csv
import os
import json


def check_duplicates(data,key):
    duplicates = dict()
    for (idx,json_dict) in enumerate(data):
        attack = json_dict[key]
        all_idx = duplicates.get(attack,[])
        all_idx.append(idx)
        duplicates[attack] = all_idx
    return duplicates

def map_sample_id(data):
    map_dict = dict()
    for (idx,json_dict) in enumerate(data):
        sample_id = json_dict['sample_id']
        map_dict[idx] = sample_id
    return map_dict


def analyze(csv_dir,data_path,init_attack_result,init_defense_result):
    with open(data_path,'r') as f:
        data = [json.loads(line) for line in f.readlines()]
    map_dict = map_sample_id(data)

    uniq_attack_ids = []
    with open(init_attack_result,'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == 'AttackID':
                continue
            if float(row[1]) > 0.25:
                continue
            #print(row[1])
            attack_id = int(row[0])
            uniq_attack_ids.append(attack_id)
    print("selected attack prompt num:%d"%(len(uniq_attack_ids)))
    uniq_defense_ids = []
    with open(init_defense_result,'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == 'DefenseID':
                continue
            defense_id = int(row[0])
            uniq_defense_ids.append(defense_id)
    print("defense prompt num:%d"%(len(uniq_defense_ids)))
    csv_list = os.listdir(csv_dir)
    defense_result = []
    attack_success_dict = dict()
    for attack_id in uniq_attack_ids:
        attack_success_dict[attack_id] = 0

    for csvfile in csv_list:
        print(csvfile)
        defense_id = int(csvfile.split('.')[0])
        if defense_id not in uniq_defense_ids:
            continue
        defence_fail_count = 0
        csv_path = os.path.join(csv_dir,csvfile)
        with open(csv_path) as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] == 'index':
                    continue 
                attack_id = int(row[-2])
                if attack_id not in uniq_attack_ids:
                    continue
                defence_fail_count += 1
                success_count = attack_success_dict[attack_id]
                attack_success_dict[attack_id] = success_count+1
        defense_result.append([defense_id,1-round(defence_fail_count/len(uniq_attack_ids),3),str(map_dict[defense_id])])
    defense_result.sort(key=lambda x:x[1],reverse=True)
    
    attack_result = list()
    for attack_id in attack_success_dict.keys():
        success_count = attack_success_dict[attack_id]
        attack_prompt = data[attack_id]['attack']
        attack_result.append([attack_id,round(success_count/len(uniq_defense_ids),3),str(map_dict[attack_id])])
    attack_result.sort(key=lambda x:x[1])
    
    with open('../Analyze_results/defense_result_select_attack.csv','w') as f:
        writer = csv.writer(f)
        writer.writerow(['DefenseID','DefenseSuccessRate','SampleID'])
        for result in defense_result:
            writer.writerow(result)
    
    with open('../Analyze_results/attack_result_select_attack.csv','w') as f:
        writer = csv.writer(f)
        writer.writerow(['AttackID','AttackSuccessRate','SampleID'])
        for result in attack_result:
            writer.writerow(result)

if __name__ == '__main__':
    csv_dir = '../Results/init/extraction'
    data_path = '../Datasets/extraction_robustness_dataset.jsonl'
    init_attack_result='../Analyze_results/attack_result_no_duplicates.csv'
    init_defense_result='../Analyze_results/defense_result_no_duplicates.csv'
    analyze(csv_dir,data_path,init_attack_result,init_defense_result)
