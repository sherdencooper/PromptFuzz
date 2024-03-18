import csv
import os
import json
import random
import pickle


seed = 0
random.seed(seed)


def create_dataset(attack_result,defense_result,focus_dataset_size,eval_dataset_size,ratio):
    distribution = dict() 
    with open(defense_result,'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == 'DefenseID':
                continue
            if float(row[1]) == 1:
                defense100 = distribution.get('defense100',list())
                defense100.append(row[0])
                distribution['defense100'] = defense100
            elif float(row[1]) > 0.8:
                defense80 = distribution.get('defense80',list())
                defense80.append(row[0])
                distribution['defense80'] = defense80
    focus_defense_100_size = int(focus_dataset_size*ratio)
    focus_defense_80_size = focus_dataset_size - focus_defense_100_size
    eval_defense_100_size = int(eval_dataset_size*ratio)
    eval_defense_80_size = eval_dataset_size - eval_defense_100_size
    defense100 = distribution['defense100']
    defense80 = distribution['defense80']            
    random.shuffle(defense100)
    random.shuffle(defense80)
    focus_defense100 = defense100[:focus_defense_100_size]
    eval_defense100 = defense100[focus_defense_100_size:(focus_defense_100_size+eval_defense_100_size)]
    focus_defense80 = defense80[:focus_defense_80_size]
    eval_defense80 = defense80[focus_defense_80_size:(focus_defense_80_size+eval_defense_80_size)]
    focus_dataset = focus_defense100+focus_defense80
    eval_dataset = eval_defense100+eval_defense80
    with open('focus_defense100.pickle','wb') as f:
        pickle.dump(focus_defense100,f) 
    with open('focus_defense80.pickle','wb') as f:
        pickle.dump(focus_defense80,f) 
    with open('eval_defense100.pickle','wb') as f:
        pickle.dump(eval_defense100,f) 
    with open('eval_defense80.pickle','wb') as f:
        pickle.dump(eval_defense80,f) 
    with open('focus_dataset.pickle','wb') as f:
        pickle.dump(focus_dataset,f) 
    with open('eval_dataset.pickle','wb') as f:
        pickle.dump(eval_dataset,f) 
    attack_dataset = [] 
    with open(attack_result,'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == 'AttackID':
                continue
            attack_dataset.append(row[0])
    with open('attack_dataset.pickle','wb') as f:
        pickle.dump(attack_dataset,f) 


if __name__ == '__main__':
    focus_dataset_size = 150
    evaluate_dataset_size = 50
    ratio = 0.2 
    defense_result='../Analyze_results/defense_result_select_attack.csv'
    attack_result='../Analyze_results/attack_result_select_attack.csv'
    create_dataset(attack_result,defense_result,focus_dataset_size,evaluate_dataset_size,ratio)
