import csv
import os
import json
import pickle



def map_sample_id(data):
    map_dict = dict()
    for (idx,json_dict) in enumerate(data):
        sample_id = json_dict['sample_id']
        map_dict[idx] = sample_id
    return map_dict


def create_dataset(data_path,id_path,save_filename):
    with open(data_path,'r') as f:
        data = [json.loads(line) for line in f.readlines()]
    with open(id_path,'rb') as f:
        ids = pickle.load(f)
    ids = [int(i) for i in ids]
    dataset = []
    for id in ids:
        dataset.append(data[id])
    save_path = os.path.join('../Datasets',save_filename)
    with open(save_path,'w') as f:
        for item in dataset:
            line = json.dumps(item)
            f.write(line+'\n')

    
if __name__ == '__main__':
    data_path = '../Datasets/extraction_robustness_dataset.jsonl'
    focus_dataset='./focus_dataset.pickle'
    eval_dataset='./eval_dataset.pickle'
    attack_dataset='./attack_dataset.pickle'
    focus_filename = 'extraction_focus_defense.jsonl'
    eval_filename = 'extraction_evaluate_defense.jsonl'
    attack_filename = 'extraction_attack.jsonl'
    create_dataset(data_path,focus_dataset,focus_filename)
    create_dataset(data_path,eval_dataset,eval_filename)
    create_dataset(data_path,attack_dataset,attack_filename)
