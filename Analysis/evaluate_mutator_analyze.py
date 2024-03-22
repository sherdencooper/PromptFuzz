import csv
import os
import json
from collections import Counter

def analyze(csv_path):
    mutator_success_count = dict()
    with open(csv_path) as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == 'index':
                continue 
            attack_id = int(row[-4])
            mutator = row[-2]
            mutator_list = mutator_success_count.get(attack_id,list())
            mutator_list.append(mutator)
            mutator_success_count[attack_id] = mutator_list
    results = []
    mutators = ['OpenAIMutatorCrossOver','OpenAIMutatorExpand','OpenAIGenerateSimilar','OpenAIMutatorRephrase','OpenAIMutatorShorten']
    for attack_id in mutator_success_count.keys():
        mutator_list = mutator_success_count[attack_id]
        counted_elements = Counter(mutator_list)
        result = [attack_id]
        for mutator in mutators:
            result.append(counted_elements[mutator])

        results.append(result)
    
    with open('../Analyze_results/evaluate_mutator_result.csv','w') as f:
        writer = csv.writer(f)
        writer.writerow(['AttackID','OpenAIMutatorCrossOver','OpenAIMutatorExpand','OpenAIGenerateSimilar','OpenAIMutatorRephrase','OpenAIMutatorShorten'])
        for result in results:
            writer.writerow(result)
        

if __name__ == '__main__':
    csv_path = '../Results/evaluate/extraction/all_results.csv'
    analyze(csv_path)
