import argparse
import pandas as pd

import pdb

def get_success_num(data):
    return sum([num for num in eval(data['results'])])

def main(args):
    df_results = pd.read_csv(args.target_file)
    df_examples = pd.DataFrame()
    mutation_list =['OpenAIMutatorCrossOver', 'OpenAIMutatorExpand', 'OpenAIMutatorGenerateSimilar', 'OpenAIMutatorRephrase', 'OpenAIMutatorShorten']
    # 遍历每行数据，并通过get_success_num计算对应results中的和，将结果添加到df_results，注意success_num是新创建的列
    for _, row in df_results.iterrows():
        df_results.loc[_, 'success_num'] = get_success_num(row)

    for mutation in mutation_list:
        filtered_df = df_results[df_results['mutation'] == mutation].sort_values(by='success_num', ascending=False)
        # 同时需要parent字段去重
        filtered_df = filtered_df.drop_duplicates(subset='parent', keep='first')
        # 将最大的20个添加到df_examples中
        df_examples = df_examples._append(filtered_df.head(20), ignore_index=True)
    # 去除success_num列
    df_examples = df_examples.drop(columns=['success_num'])
    df_examples.to_csv(args.output_file, index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Testing parameters')
    parser.add_argument('--target_file', type=str, default='./Results/evaluate/hijacking/hijacking_evaluation_all_results_add_2.csv',
                        help='The file to be evaluated')
    parser.add_argument('--init_file', type=str, default='./Datasets/hijacking_evaluate_seed.jsonl',
                        help='The init file to get the index2sample_id')
    parser.add_argument('--output_file', type=str, default='./Results/evaluate/hijacking/hijacking_evaluate_example.csv',
                        help='The output file to save the results')

    args = parser.parse_args()

    main(args)