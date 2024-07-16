import os
import json
import pdb
import argparse
import pandas as pd


def main(args):
    # 读取focus_pool_file文件
    df_focus_pool = pd.read_csv(args.focus_pool_file)
    # 读取sample_id，按顺序读取前四十个，保存到focus_id中
    focus_id = df_focus_pool['SampleID'].tolist()[:40]
    # pdb.set_trace()
    with open(args.init_file, 'r') as f:
        data = f.readlines()
    data = [json.loads(line) for line in data]
    # 通过focus_id在data中获取对应的数据
    # 仅获取前四十个
    focus_data = [d for d in data if d['sample_id'] in focus_id]
    # 保存focus_data到jsonl文件中
    with open(args.output_file, 'w') as f:
        for d in focus_data:
            f.write(json.dumps(d) + '\n')
    


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Testing parameters')
    parser.add_argument('--focus_pool_file', type=str, default='./Results/evaluate/hijacking/hijacking_attack_ranking.csv',)
    parser.add_argument('--init_file', type=str, default='./Datasets/hijacking_evaluate_seed.jsonl',)
    parser.add_argument('--output_file', type=str, default='./Datasets/hijacking_focus_seed.jsonl',)

    args = parser.parse_args()

    main(args)