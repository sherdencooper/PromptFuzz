import json
import argparse
import pandas as pd

def get_index2sample_id(target_file_path):
    # Get the index2sample_id mapping
    #@param target_file_path: The path to the target file
    #@return index2sample_id: The index2sample_id mapping

    index2sample_id = {}
    with open(target_file_path, 'r') as f:
        for line in f.readlines():
            sample_id = json.loads(line)['sample_id']
            index2sample_id[len(index2sample_id)] = sample_id
    return index2sample_id

def main(args):
    results = {}
    df_results = pd.read_csv(args.target_file)
    index2sample_id = get_index2sample_id(args.init_file)

    # Get the attack success rate for each parent
    for parent in range(0, 80):
        df_temp = df_results[df_results['parent'] == parent]
        sum_attack = 0
        for _, row in df_temp.iterrows():
            sum_attack += sum([num for num in eval(row['results'])])
        results[parent] = {
            'AttackID': parent,
            'AttackSuccessRate': round(sum_attack / args.defense_num, 4), 
            'SampleID': str(index2sample_id[parent])
        }
    df = pd.DataFrame(results).T
    df = df.sort_values(by='AttackSuccessRate', ascending=False)

    # Get the topN focus samples
    focus_id = df['SampleID'].tolist()[:args.topN]
    with open(args.init_file, 'r') as f:
        data = f.readlines()
    data = [json.loads(line) for line in data]
    focus_data = [d for d in data if d['sample_id'] in focus_id]
    with open(args.output_file, 'w') as f:
        for d in focus_data:
            f.write(json.dumps(d) + '\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Testing parameters')
    parser.add_argument('--target_file', type=str, default='./Results/preparation/hijacking/all_results.csv', help='The file to be evaluated')
    parser.add_argument('--output_file', type=str, default='./Datasets/hijacking_focus_seed.jsonl',)
    parser.add_argument('--init_file', type=str, default='./Datasets/hijacking_preparation_seed.jsonl', help='The init file to get the index2sample_id')
    parser.add_argument('--topN', type=int, default=40, help='The number of focus samples')
    parser.add_argument('--defense_num', type=int, default=50, help='The number of defenses')


    args = parser.parse_args()

    main(args)