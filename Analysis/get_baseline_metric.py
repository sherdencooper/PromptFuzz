import pdb
import pandas as pd
import numpy as np
import os
import glob

def read_csv_files(path):
    # 获取目标文件夹下的所有csv文件
    all_files = glob.glob(os.path.join(path, "*.csv"))
    # 读取所有csv文件
    # 有的文件中，只有一行，有的有多行，在合并时，如果有多行，只关心第一行
    # 合并的时候，需要加上新的一列，这一列中的内容是文件名，新列在第一列
    df = pd.DataFrame()
    for file in all_files:
        file_name = os.path.basename(file).split('.')[0]
        temp_df = pd.read_csv(file, nrows=1)
        temp_df['defense_id'] = file_name
        df = pd.concat([temp_df, df])
    return df

def get_asr_list(df, parent):
    
    # 创建一个长度为150的列表，初始化为0
    asr_list = [0] * 150
    # 获取当前parent对应的所有defense_id
    defense_ids = df[df['parent'] == parent]['defense_id'].tolist()
    # 设置对应的索引为1
    for defense_id in defense_ids:
        if 0 <= defense_id < 150:
            asr_list[defense_id] = 1
    return asr_list

def get_metric_normal(file_path, topK=5):
    
    df = pd.read_csv(file_path)

    if 'lmi' in file_path.lower() or 'gcg' in file_path.lower():
        unique_parents = df.drop_duplicates(subset=['parent'])['parent'].tolist()
        attack_list = []
        for parent in unique_parents:
            asr_list = get_asr_list(df, parent)
            attack_list.append(asr_list)
        df_new = pd.DataFrame({
            'AttackSuccessList': attack_list,
            'AttackSuccessRate': [sum(attack_list[i]) / 150 for i in range(len(unique_parents))],
        })
        # 保存到csv文件
        # df_new.to_csv('./Results/focus/hijacking/baseline_LMI/debug.csv', index=False)
    else:
    
        df_new = pd.DataFrame({'AttackID': df['index'], 
                               'AttackSuccessList': df['results'].apply(lambda x: eval(x)),
                               'AttackSuccessNum': df['results'].apply(lambda x: sum(eval(x))), 
                               'AttackSuccessRate': df['results'].apply(lambda x: sum(eval(x))/150), 
                               'ParentAttackID': df['parent'], 
                               'AttackPrompt': df['prompt']})
    # get best asr
    best_asr = df_new['AttackSuccessRate'].max()

    # get ensemble asr
    df_new = df_new.sort_values(by='AttackSuccessRate', ascending=False)
    ensemble_success_list = np.bitwise_or.reduce(df_new['AttackSuccessList'].tolist()[:topK])
    ensemble_asr = sum(ensemble_success_list) / len(ensemble_success_list)
    
    # get coverage metric
    all_success_lists = df_new['AttackSuccessList'].tolist()
    combined_success_list = [any(col) for col in zip(*all_success_lists)]
    coverage_metric = sum(combined_success_list) / len(combined_success_list)

    return round(best_asr, 4), round(ensemble_asr, 4), round(coverage_metric, 4)

def main(file_paths):
    # Record the best ASR, ensemble ASR, and coverage metric for each file
    results = []
    for file_path in file_paths:
        # Get uniform result & bestASR
        best_asr, ensemble_asr, coverage_metric = get_metric_normal(file_path)
        # Print the results
        print(f"File {file_path}:")
        print(f"Best ASR: {best_asr}")
        print(f"Ensemble ASR: {ensemble_asr}")
        print(f"Coverage Metric: {coverage_metric}")
        print()
        results.append((file_path ,best_asr, ensemble_asr, coverage_metric))

    df = pd.DataFrame(results, columns=['FileID', 'BestASR', 'EnsembleASR', 'CoverageMetric'])
    df.to_csv('./Results/focus/hijacking/baseline_all/metric_results.csv', index=False)
    

    
if __name__ == '__main__':
    # 处理GCG和LMI
    df_LMI = read_csv_files("./Results/focus/hijacking/baseline_LMIGCG/lmi_baseline_all_defenses") # GCG和LMI存放xx.csv的文件夹
    df_GCG = read_csv_files("./Results/focus/hijacking/baseline_LMIGCG/gcg_baseline_all_defenses") # GCG和LMI存放xx.csv的文件夹
    lmi_csv_path = "./Results/focus/hijacking/baseline_LMIGCG/hijacking_init_results_LMI_debug_3.csv"
    gcg_csv_path = "./Results/focus/hijacking/baseline_LMIGCG/hijacking_init_results_GCG_debug_3.csv"
    df_GCG.to_csv(gcg_csv_path)
    df_LMI.to_csv(lmi_csv_path)

    # 处理Initial_seed


    file_paths = [gcg_csv_path,
                  lmi_csv_path,
                  'Results/focus/hijacking/baseline_gptfuzzer/all_results.csv',
                  './Results/focus/hijacking/all_defense/hijacking_all_results_bk_1.csv',
                  './Results/focus/hijacking/all_defense/hijacking_all_results_bk_2.csv',
                  './Results/focus/hijacking/all_defense/hijacking_all_results_bk_3.csv',
                  ]
    
    main(file_paths)

