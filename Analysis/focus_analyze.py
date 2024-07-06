import csv
import os
import json
import ast
import sys

csv.field_size_limit(sys.maxsize)

def analyze(csv_path):
    attack_result = list()
    with open(csv_path) as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == 'index':
                continue 
            attack_id = int(row[0])
            prompt = row[1]
            parent_attack_id = int(row[-4])
            attack_results = ast.literal_eval(row[-3])
            success_attack = sum(attack_results)
            total_attack = len(attack_results)
    
            attack_result.append([attack_id,success_attack,round(success_attack/total_attack,3),parent_attack_id,prompt])
    attack_result.sort(key=lambda x:x[1],reverse=True)
    
    
    with open('../Analyze_results/GPTFuzzer_focus_result.csv','w') as f:
        writer = csv.writer(f)
        writer.writerow(['AttackID','AttackSuccessNum','AttackSuccessRate','ParentAttackID','AttackPrompt'])
        for result in attack_result:
            writer.writerow(result)
    

if __name__ == '__main__':
    #csv_path = '../Results/focus/extraction/cs_da/all_results.csv'
    csv_path = '/home/hwmiao/PromptFuzz/PromptFuzz/Results/focus/extraction/all_results.csv'
    #total_attack = 150
    analyze(csv_path)
