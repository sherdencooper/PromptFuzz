import pdb
import json
import pandas as pd

import os
import glob

def read_csv_files(path):

    all_files = glob.glob(os.path.join(path, "*.csv"))
    df = pd.DataFrame()
    for file in all_files:
        file_name = os.path.basename(file).split('.')[0]
        temp_df = pd.read_csv(file, nrows=1)
        temp_df['defense_id'] = file_name
        df = pd.concat([temp_df, df])
    return df

df = read_csv_files('Results/focus/hijacking/rate100_cost_finetuned_re/1000/run_3/result_rate100_finetuned_cost_1000')
df.to_csv('Results/focus/hijacking/rate100_cost_finetuned_re/1000/run_3/ft_rate100_cost3.csv', index=False)
