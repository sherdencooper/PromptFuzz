import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import ast
import argparse

def process_iteration_by_parent(df):
    iterations = {}
    part_data = []
    current_parent = 0
    iteration = 0
    for _, row in df.iterrows():
        if row['parent'] == current_parent:
            part_data.append(row['results'])
        else:
            iterations[iteration] = part_data[:] # 保存上一个iteration的数据
            current_parent = row['parent']
            iteration += 1
            part_data.append(row['results'])

    return iterations

def process_iterations_by_query(df):
    iterations = {}
    part_data = []
    part_query= 750
    iter_num = 1
    for _, row in df.iterrows():
        if row['query'] < part_query:
            # iteration part 内部添加数据
            part_data.append(row['results'])
        elif row['query'] < part_query + 750:
            # 进入下一个iteration，顺利更新part_query
            iterations[iter_num] = part_data[:] # 保存上一个iteration的数据
            part_data.append(row['results'])    # 添加这个数据
            part_query += 750               # 更新part_query_num
            iter_num += 1
        else:
            # 空转iteration，反复添加上一步的part数据，并更新part_query_num
            while row['query'] > part_query :
                iterations[iter_num] = part_data[:]
                part_query += 750               # 更新part_query_num
                iter_num += 1
    return iterations

def std_numpy(x):
    return round(np.std(x), 5)

def get_metric(attack_list, topK=5):
    # pdb.set_trace() 
    df_new = pd.DataFrame({
        'AttackSuccessList': [ast.literal_eval(x) for x in attack_list],
        'AttackSuccessRate': [sum(ast.literal_eval(attack_list[i])) / 150 for i in range(len(attack_list))],
    })
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

def process_all_data(file_paths, method='promptfuzz', mode='hijacking', show=False):
    df_list = []
    for file_path in file_paths:
        df = pd.read_csv(file_path)
        iterations = process_iterations_by_query(df)
        best_asr_list = []
        ensemble_asr_list = []
        coverage_metric_list = []
        for i in iterations:
            best_asr, ensemble_asr, coverage_metric = get_metric(iterations[i])
            best_asr_list.append(best_asr)
            ensemble_asr_list.append(ensemble_asr)
            coverage_metric_list.append(coverage_metric)
            if show:
                print(f'iteration {i}:')
                print(f'best_asr: {best_asr}')
                print(f'ensemble_asr: {ensemble_asr}')
                print(f'coverage_metric: {coverage_metric}')
                print()
        if len(iterations) < 201: # Alignment
            # 将最后一个复制，让整体长度为201
            best_asr_list.extend([best_asr] * (201 - len(iterations)))
            ensemble_asr_list.extend([ensemble_asr] * (201 - len(iterations)))
            coverage_metric_list.extend([coverage_metric] * (201 - len(iterations)))


        # build dataframe by best_asr_list, ensemble_asr_list, coverage_metric_list
        df = pd.DataFrame({
            'iteration': range(1, 202),
            'best_asr': best_asr_list,
            'ensemble_asr': ensemble_asr_list,
            'coverage_metric': coverage_metric_list
        })
        df_list.append(df)
        if method == 'promptfuzz':
            df.to_csv(file_path.replace('.csv', '_processed.csv'), index=False)
        else:
            df.to_csv(f'./datasets/{mode}_gptfuzzer_result.csv', index=False)
    # 针对df_list中的df，分别求其在每个iteration的best_asr、ensemble_asr、coverage_metric的平均值、标准差
    combined_df = pd.concat(df_list, ignore_index=True)
    result_df = combined_df.groupby('iteration').agg({'best_asr': ['mean', std_numpy],
                                                      'ensemble_asr': ['mean', std_numpy],
                                                      'coverage_metric': ['mean', std_numpy]}).reset_index()
    
    result_df = result_df.round(5)
    if method == 'promptfuzz':
        result_df.to_csv(f'./datasets/{mode}_promptfuzz_result.csv', index=False)
    print(result_df)
    return result_df

if __name__ == "__main__":
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--file_paths', type=str, nargs='+', help='file paths')
    # parser.add_argument('--method', type=str, default='promptfuzz', help='method')
    # parser.add_argument('--mode', type=str, default='hijacking', help='mode')
    # parser.add_argument('--show', type=bool, default=False, help='show')
    # args = parser.parse_args()

    hijacking_file_paths_promptfuzz = ['./datasets/hijacking_all_results_bk_1.csv', 
                                   './datasets/hijacking_all_results_bk_2.csv',
                                   './datasets/hijacking_all_results_bk_3.csv']
    extraction_file_paths_promptfuzz = ['./datasets/extraction_all_results_1.csv', 
                                        # './datasets/extraction_all_results_2.csv',
                                        #'./datasets/extraction_all_results_3.csv'
                                        ]

    hijacking_file_paths_gptfuzzer = ['./datasets/hijacking_gptfuzzer_all_results.csv']
    extraction_file_paths_gpftuzzer = ['./datasets/extraction_gptfuzzer_all_results.csv']

    # hijacking_promptfuzz = process_all_data(extraction_file_paths_promptfuzz, method='promptfuzz', mode='hijacking')

    # hijacking_gptfuzzer = process_all_data(extraction_file_paths_gpftuzzer, method='gptfuzzer', mode='hiijacking')

    extraction_promptfuzz = process_all_data(extraction_file_paths_promptfuzz, method='promptfuzz', mode='extraction')

    # extraction_gptfuzzer = process_all_data(extraction_file_paths_gpftuzzer, method='gptfuzzer', mode='extraction')