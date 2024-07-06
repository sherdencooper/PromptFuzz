import csv
import os
import json
import pandas as pd

def search_parent(df, attack_index):
   row = df[df['AttackID']==attack_index]
   parent_index = int(row['ParentAttackID'])
   if parent_index < 40:
       return parent_index
   else:
       return search_parent(df, parent_index)
       




if __name__ == '__main__':
    csv_path = '/home/hwmiao/PromptFuzz/PromptFuzz/Analyze_results/focus_attack_result.csv'
    attack_seed = '/home/hwmiao/PromptFuzz/PromptFuzz/Datasets/extraction_focus_seed.jsonl'
    df = pd.read_csv(csv_path)
    with open(attack_seed) as f:
        lines = f.readlines()
    attacks = [json.loads(line) for line in lines]
    originID_list = []
    originPrompt_list = []
    for index, row in df.iterrows():
        attack_index = row['AttackID']
        attack_prompt = row['AttackPrompt']
        origin_index = search_parent(df, attack_index)
        origin_prompt = attacks[origin_index]['attack']
        originID_list.append(origin_index)
        originPrompt_list.append(origin_prompt)
    df = df.assign(OriginID=originID_list)
    df = df.assign(OriginPrompt=originPrompt_list)
    df.to_csv('../Analyze_results/origin.csv',index=False) 
