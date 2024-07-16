import os
import argparse
import pandas as pd
import numpy as np

def main(args):
    # get attack id
    df_attack = pd.read_csv(args.attack_pool)
    attack_ids = df_attack['attackID'].tolist()
    # get defense id
    df_defense = pd.read_csv(args.defense_pool)
    defense_ids = df_defense['defenseID'].tolist()
     # attack_list初始化成个数为len(attack_ids),元素为0的dataframe
    attack_list = [[0 for _ in range(len(defense_ids))] for _ in range(len(attack_ids))]
    # loop csv file by defense id

    for idx, defense_id in enumerate(defense_ids):
        # get defense id
        df_defense = pd.read_csv(os.path.join(args.target_folder_path, f'{defense_id}'))
        # get parent id
        parent_ids = df_defense['parent'].tolist()
        # count the number of attack id in parent id
        for parent_id in parent_ids:
            if parent_id in attack_ids:
                attack_list[attack_ids.index(parent_id)][idx] += 1
        
    # attack_list转换成dataframe，行为attack_ids，列为对应的list
    df = pd.DataFrame({
        'id': attack_ids,
        'AttackSuccessList': attack_list,
        'AttackSuccessRate': [sum(attack_list[i]) / len(defense_ids) for i in range(len(attack_ids))],
    })
    # get best ASR
    bestASR = df['AttackSuccessRate'].max()
    # get ensemble asr
    df_new = df.sort_values(by='AttackSuccessRate', ascending=False)
    ensemble_success_list = np.bitwise_or.reduce(df_new['AttackSuccessList'].tolist()[:args.topK])
    ensemble_asr = sum(ensemble_success_list) / len(ensemble_success_list)
    
    # get coverage metric
    all_success_lists = df_new['AttackSuccessList'].tolist()
    combined_success_list = [any(col) for col in zip(*all_success_lists)]
    coverage_metric = sum(combined_success_list) / len(combined_success_list)

    print(f'Best ASR: {round(bestASR, 4)}, Ensemble ASR: {round(ensemble_asr, 4)}, Coverage Metric: {round(coverage_metric, 4)}')
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fuzzing parameters')
    parser.add_argument('--attack_pool', type=str, default='./Results/init/eval_hijacking_fixed/sampled_attack.csv',help='to get attack id, e.g., 205')
    parser.add_argument('--defense_pool', type=str, default='./Results/init/eval_hijacking_fixed/sampled_focus_defense_by_attackpool.csv', help='to get defense id, e.g., 324.csv')
    parser.add_argument('--target_folder_path', type=str, default='./Results/init/hijacking_fixed', help='to loop csv file by defense id')
    parser.add_argument('--save_folder_path', type=str, default='Results/init/eval_hijacking_fixed', help='The path of the folder that contains the csv files') 
    parser.add_argument('--topK', type=int, default=5, help='topK defense to ensemble')

    args = parser.parse_args()
    main(args)