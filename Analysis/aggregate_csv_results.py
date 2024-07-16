import pdb
import json
import pandas as pd

# 读取目标文件夹下的多个csv文件，多个文件的内容合并，并且在每个文件的内容前面加上文件名
import os
import glob

# 读取目标文件夹下的所有csv文件
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

# 读取目标文件夹下的所有csv文件
df = read_csv_files('Results/focus/hijacking/rate100_cost_finetuned_re/1000/run_3/result_rate100_finetuned_cost_1000')
# 保存结果
df.to_csv('Results/focus/hijacking/rate100_cost_finetuned_re/1000/run_3/ft_rate100_cost3.csv', index=False)
