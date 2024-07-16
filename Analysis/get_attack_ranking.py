
import json
import argparse
import pdb
import pandas as pd

def get_index2sample_id(target_file_path):
    # 读取jsonl文件
    index2sample_id = {}
    with open(target_file_path, 'r') as f:
        for line in f.readlines():
            sample_id = json.loads(line)['sample_id']
            index2sample_id[len(index2sample_id)] = sample_id
    return index2sample_id

def main(args):
    # 构造一个pandas的对象，用于保存结果，其中包含id,results和parent_id三列
    results = {}
    # 读取csv 文件
    df_results = pd.read_csv(args.target_file)
    # 获取df_init的index2sample_id映射
    index2sample_id = get_index2sample_id(args.init_file)

    for parent in range(0, 80):
        # 将parent为i的行筛选出来，并且保存到df_temp中
        df_temp = df_results[df_results['parent'] == parent]
        all_num = 50
        print(all_num)
        # 便利df_temp中的每一行，并将results列中的list求和计算，并且累计所有的列，注意results列中的数据是list，所以需要先求和
        sum_attack = 0
        for _, row in df_temp.iterrows():
            sum_attack += sum([num for num in eval(row['results'])])
        # 将parent，parent_id和sum_attack保存到results中
        results[parent] = {
            'AttackID': parent,
            'AttackSuccessRate': round(sum_attack / all_num, 4), 
            'SampleID': str(index2sample_id[parent])
        }
    # 打印results列表
    # print(results)
    # 保存results到csv文件中
    df = pd.DataFrame(results).T
    # 按照sum_attack排序
    df = df.sort_values(by='AttackSuccessRate', ascending=False)
    df.to_csv('./Results/evaluate/hijacking/hijacking_sum_attack.csv', index=False)

        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Testing parameters')
    parser.add_argument('--target_file', type=str, default='./Results/evaluate/hijacking/hijacking_evaluation_all_results.csv', help='The file to be evaluated')
    parser.add_argument('--init_file', type=str, default='./Datasets/hijacking_evaluate_seed.jsonl', help='The init file to get the index2sample_id')

    args = parser.parse_args()

    main(args)