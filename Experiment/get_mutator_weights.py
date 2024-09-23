import argparse
import pandas as pd

def main(args):
    
    df_mutator = pd.DataFrame(columns=['AttackID', 'OpenAIMutatorCrossOver', 'OpenAIMutatorExpand', 'OpenAIMutatorGenerateSimilar', 'OpenAIMutatorRephrase', 'OpenAIMutatorShorten'])
    df_results = pd.read_csv(args.target_file)

    for _, row in df_results.iterrows():
        parent = row['parent']
        mutation = row['mutation']
        if parent not in df_mutator['AttackID'].values:
            df_mutator = df_mutator._append({'AttackID': parent, 'OpenAIMutatorCrossOver': 0, 'OpenAIMutatorExpand': 0, 'OpenAIMutatorGenerateSimilar': 0, 'OpenAIMutatorRephrase': 0, 'OpenAIMutatorShorten': 0}, ignore_index=True)
        df_mutator.loc[df_mutator['AttackID'] == parent, mutation] += 1
    
    df_mutator['Total'] = df_mutator['OpenAIMutatorCrossOver'] + df_mutator['OpenAIMutatorExpand'] + df_mutator['OpenAIMutatorGenerateSimilar'] + df_mutator['OpenAIMutatorRephrase'] + df_mutator['OpenAIMutatorShorten']
    df_mutator.to_csv(args.output_file, index=False)
    
    df_mutator_sum = df_mutator.sum()
    df_mutator_sum = df_mutator_sum / df_mutator_sum['Total']
    print(df_mutator_sum)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Testing parameters')
    parser.add_argument('--target_file', type=str, default=None, help='The file to be evaluated')
    parser.add_argument('--output_file', type=str, default=None, help='The output file to save the results')

    args = parser.parse_args()

    main(args)