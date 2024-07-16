
import os
import shutil
import pandas as pd

# 将上述的程序封装为函数
def get_uniform_result(file_path, save_path):
    df = pd.read_csv(file_path)
    # 在计算AttackSuccessNum的时候使用sum([num for num in eval(row[1]['results'])])

    df_new = pd.DataFrame({'AttackID': df['index'], 
                           'AttackSuccessNum': df['results'].apply(lambda x: sum(eval(x))), 
                           'AttackSuccessRate': df['results'].apply(lambda x: sum(eval(x))/150), 
                           'ParentAttackID': df['parent'], 
                           'AttackPrompt': df['prompt']})
    # 按照AttackSuccessRate进行排序
    df_new = df_new.sort_values(by='AttackSuccessRate', ascending=False)
    df_new.to_csv(save_path, index=False)

def copy_and_rename_csv(input_dir, output_dir):
    """
    Copies all 'all_results.csv' files from various subdirectories in 'input_dir' 
    to 'output_dir' and renames them based on their parent directory.

    Args:
    input_dir (str): The directory containing the subdirectories with the CSV files.
    output_dir (str): The directory where the copied and renamed files will be stored.
    """
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Walk through the input directory
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file == 'all_results.csv':
                # Determine the subdirectory name (assuming it's the format 'as...')
                path_parts = root.split(os.path.sep)
                as_folder = next((part for part in path_parts if part.startswith('as')), None)
                if as_folder:
                    # Create a new file name based on the subdirectory
                    new_file_name = f"{as_folder}_all_results.csv"
                    # Construct full file paths
                    source_file = os.path.join(root, file)
                    destination_file = os.path.join(output_dir, new_file_name)
                    # Copy the file to the new location with the new name
                    shutil.copy(source_file, destination_file)
                    print(f"Copied and renamed {source_file} to {destination_file}")


if __name__ == '__main__':

    # 1. 为ablation_study_4_23中的所有文件生成uniform_result
    # input_dir = './Results/focus/hijacking/ablation/ablation_study_4_23'
    # output_dir = './Results/focus/hijacking/ablation/all_results'
    # save_path = './Results/focus/hijacking/ablation/ablation_study_4_23_uniform'

    # copy_and_rename_csv(input_dir, output_dir)

    # # 遍历文件夹内的所有文件，并调用get_uniform_result
    # for root, dirs, files in os.walk(output_dir):
    #     for file in files:
    #         file_path = os.path.join(root, file)
    #         save_path = file_path.replace('uniform_all_results', 'uniform_result')
    #         get_uniform_result(file_path, save_path)
    #         print(f"Processed {file_path} and saved to {save_path}")

    # 2. 为all_defnse中的所有文件生成uniform_result

    # target_dir = './Results/focus/hijacking/all_defense'
    # save_dir = './Results/focus/hijacking/all_defense/uniform_all_defense'
    # # 遍历文件夹内的所有文件，并调用get_uniform_result
    # for root, dirs, files in os.walk(target_dir):
    #     for file in files:
    #         file_path = os.path.join(root, file)
    #         save_path = file_path.replace('all_defense', 'all_defense/uniform_all_defense')
    #         get_uniform_result(file_path, save_path)
    #         print(f"Processed {file_path} and saved to {save_path}")

    # 3. 为文件夹内的所有csv文件生成uniform_result
    # target_folder = './Results/focus/extraction/ablation_extraction/all_results/'
    # for file in os.listdir(target_folder):
    #     if file.endswith('.csv'):
    #         path = target_folder + file
    #         save_path = path.replace('all_results', 'uniform_results')
    #         get_uniform_result(path, save_path)
    #         print(f"Processed {path} and saved to {save_path}")
    file_path = 'Results/focus/hijacking/ablation/ablation_study_5_16/all_results_5_16.csv'
    save_path = 'Results/focus/hijacking/ablation/ablation_study_5_16/uniform_results_5_16.csv'
    get_uniform_result(file_path, save_path)
