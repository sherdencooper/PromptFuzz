import argparse
import pandas as pd

def main(args):
    # 创建一个pandas 对象，其中为['AttackID', 'OpenAIMutatorCrossOver', 'OpenAIMutatorExpand', 'OpenAIGenerateSimilar', 'OpenAIMutatorRephrase', 'OpenAIMutatorShorten']。
    # 其中AttackID是target_file中的parent列，并且Attack_ID在target_file中的parent列中是有重复的。同时相同的Attack_ID行对应的mutator是不同的。
    # 需要记一个总数。后面的几列是来自target_file中的mutator列，统计每个mutator的数量
    df_mutator = pd.DataFrame(columns=['AttackID', 'OpenAIMutatorCrossOver', 'OpenAIMutatorExpand', 'OpenAIMutatorGenerateSimilar', 'OpenAIMutatorRephrase', 'OpenAIMutatorShorten'])
    # 读取csv文件
    df_results = pd.read_csv(args.target_file)
    # 遍历df_results
    for index, row in df_results.iterrows():
        # 读取parent列
        parent = row['parent']
        # 读取mutator列
        mutation = row['mutation']
        # 如果df_mutator中没有parent的行，则添加一行
        if parent not in df_mutator['AttackID'].values:
            df_mutator = df_mutator._append({'AttackID': parent, 'OpenAIMutatorCrossOver': 0, 'OpenAIMutatorExpand': 0, 'OpenAIMutatorGenerateSimilar': 0, 'OpenAIMutatorRephrase': 0, 'OpenAIMutatorShorten': 0}, ignore_index=True)
        # 统计mutator的数量
        df_mutator.loc[df_mutator['AttackID'] == parent, mutation] += 1
    # 在df的最后一列上加上一个总数
    df_mutator['Total'] = df_mutator['OpenAIMutatorCrossOver'] + df_mutator['OpenAIMutatorExpand'] + df_mutator['OpenAIMutatorGenerateSimilar'] + df_mutator['OpenAIMutatorRephrase'] + df_mutator['OpenAIMutatorShorten']
    # 保存df_mutator到csv文件中
    df_mutator.to_csv(args.output_file, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Testing parameters')
    parser.add_argument('--target_file', type=str, default='./Results/evaluate/hijacking/hijacking_evaluation_all_results.csv', help='The file to be evaluated')
    # parser.add_argument('--init_file', type=str, default='./Datasets/hijacking_evaluate_seed.jsonl', help='The init file to get the index2sample_id')
    parser.add_argument('--output_file', type=str, default='./Results/evaluate/hijacking/hijacking_evaluation_mutator_sum.csv', help='The output file to save the results')

    args = parser.parse_args()

    main(args)