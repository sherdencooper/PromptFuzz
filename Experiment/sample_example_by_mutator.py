import argparse
import pandas as pd

def get_success_num(data):
    # Get the number of successful attacks
    return sum([num for num in eval(data['results'])])

def main(args):
    df_results = pd.read_csv(args.target_file)
    df_examples = pd.DataFrame()
    mutation_list =['OpenAIMutatorCrossOver', 'OpenAIMutatorExpand', 'OpenAIMutatorGenerateSimilar', 'OpenAIMutatorRephrase', 'OpenAIMutatorShorten']
    for _, row in df_results.iterrows():
        df_results.loc[_, 'success_num'] = get_success_num(row)

    for mutation in mutation_list:
        filtered_df = df_results[df_results['mutation'] == mutation].sort_values(by='success_num', ascending=False)
        filtered_df = filtered_df.drop_duplicates(subset='parent', keep='first')
        df_examples = df_examples._append(filtered_df.head(args.top_k), ignore_index=True)
    df_examples = df_examples.drop(columns=['success_num'])
    df_examples.to_csv(args.output_file, index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Testing parameters')
    parser.add_argument('--target_file', type=str, default='./Results/preparation/hijacking/all_defenses.csv',
                        help='The file to be evaluated')
    parser.add_argument('--init_file', type=str, default='./Datasets/hijacking_preparation_seed.jsonl',
                        help='The init file to get the index2sample_id')
    parser.add_argument('--output_file', type=str, default='./Results/preparation/hijacking/hijacking_few_shot_example.csv',
                        help='The output file to save the results')
    parser.add_argument('--top_k', type=int, default=20, help='The number of examples to be saved')

    args = parser.parse_args()

    main(args)