import csv
import os
import json
import pickle


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


def analyze(csv_dir,data_path,defense_dataset_path,attack_dataset_path):
    with open(data_path,'r') as f:
        data = [json.loads(line) for line in f.readlines()]
    map_dict = map_sample_id(data)
    with open(defense_dataset_path,'rb') as f:
        defense_data = pickle.load(f)
    defense_ids = [int(i) for i in defense_data]
    with open(attack_dataset_path,'rb') as f:
        attack_data = pickle.load(f)
    attack_ids = [int(i) for i in attack_data]
    attack_nums = len(attack_ids)
    csv_list = os.listdir(csv_dir)
    defense_result = []
    attack_success_dict = dict()
    for attack_id in attack_ids:
        attack_success_dict[attack_id] = 0

    for csvfile in csv_list:
        print(csvfile)
        defense_id = int(csvfile.split('.')[0])
        if defense_id not in defense_ids:
            continue
        defense_fail_count = 0
        csv_path = os.path.join(csv_dir,csvfile)
        with open(csv_path) as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] == 'index':
                    continue 
                attack_id = int(row[-2])
                if attack_id not in attack_ids:
                    continue
                defense_fail_count += 1
                success_count = attack_success_dict[attack_id]
                attack_success_dict[attack_id] = success_count+1
        defense_result.append([defense_id,1-round(defense_fail_count/len(attack_ids),3),str(map_dict[defense_id])])
    defense_result.sort(key=lambda x:x[1],reverse=True)
    
    attack_result = list()
    for attack_id in attack_success_dict.keys():
        success_count = attack_success_dict[attack_id]
        attack_prompt = data[attack_id]['attack']
        attack_result.append([attack_id,round(success_count/len(defense_ids),3),str(map_dict[attack_id])])
    attack_result.sort(key=lambda x:x[1])
    defense_result_path = os.path.join('../Analyze_results',os.path.basename(defense_dataset_path).split('.')[0]+'_result.csv')
    with open(defense_result_path,'w') as f:
        writer = csv.writer(f)
        writer.writerow(['DefenseID','DefenseSuccessRate','SampleID'])
        for result in defense_result:
            writer.writerow(result)
    
    attack_result_path = os.path.join('../Analyze_results',os.path.basename(attack_dataset_path).split('.')[0]+'_result.csv')
    with open(attack_result_path,'w') as f:
        writer = csv.writer(f)
        writer.writerow(['AttackID','AttackSuccessRate','SampleID'])
        for result in attack_result:
            writer.writerow(result)

if __name__ == '__main__':
    csv_dir = '../Results/init/extraction'
    data_path = '../Datasets/extraction_robustness_dataset.jsonl'
    focus_dataset='./focus_dataset.pickle'
    eval_dataset='./eval_dataset.pickle'
    attack_dataset='./attack_dataset.pickle'
    analyze(csv_dir,data_path,focus_dataset,attack_dataset)
    analyze(csv_dir,data_path,eval_dataset,attack_dataset)
