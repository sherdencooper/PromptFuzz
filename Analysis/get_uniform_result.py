
import os
import shutil
import pandas as pd

def get_uniform_result(file_path, save_path):
    # Read the csv file
    #@param file_path: the path to the csv file
    #@param save_path: the path to save the new csv file

    df = pd.read_csv(file_path)
    df_new = pd.DataFrame({'AttackID': df['index'], 
                           'AttackSuccessNum': df['results'].apply(lambda x: sum(eval(x))), 
                           'AttackSuccessRate': df['results'].apply(lambda x: sum(eval(x))/150), 
                           'ParentAttackID': df['parent'], 
                           'AttackPrompt': df['prompt']})
    
    df_new = df_new.sort_values(by='AttackSuccessRate', ascending=False)
    df_new.to_csv(save_path, index=False)

def copy_and_rename_csv(input_dir, output_dir):
    # Copy and rename all_results.csv files from subdirectories to the output directory
    #@param input_dir: the directory containing the subdirectories with all_results.csv files
    #@param output_dir: the directory to copy the renamed files to
    
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
    file_path = 'Results/focus/hijacking/ablation/ablation_study_5_16/all_results_5_16.csv'
    save_path = 'Results/focus/hijacking/ablation/ablation_study_5_16/uniform_results_5_16.csv'
    get_uniform_result(file_path, save_path)
