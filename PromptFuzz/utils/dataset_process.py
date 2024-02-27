import json
import random
random.seed(42)


def process_dataset(file_path, split_percentage, save_folder):
    # load the jsonl dataset
    with open(file_path, 'r') as f:
        dataset = [json.loads(line) for line in f]
    # split the dataset randomly
    random.shuffle(dataset)
    split_index = int(len(dataset) * split_percentage)
    train_dataset = dataset[:split_index]
    test_dataset = dataset[split_index:]
    # save the datasets to the save folder
    mode = file_path.split('/')[-1].split('_')[0]
    train_save_path = save_folder + mode + '_focus.jsonl'
    test_save_path = save_folder + mode + '_evaluate.jsonl'
    with open(train_save_path, 'w') as f:
        for data in train_dataset:
            f.write(json.dumps(data) + '\n')
    with open(test_save_path, 'w') as f:
        for data in test_dataset:
            f.write(json.dumps(data) + '\n')
    print(f"Train dataset saved to {train_save_path}")
    print(f"Test dataset saved to {test_save_path}")

    
    
    
    
if __name__ == "__main__":
    extract_path = '../../Datasets/extraction_robustness_dataset.jsonl'
    hijacking_path = '../../Datasets/hijacking_robustness_dataset.jsonl'
    split_percentage = 0.9
    save_folder = '../../Datasets/'
    process_dataset(extract_path, split_percentage, save_folder)
    process_dataset(hijacking_path, split_percentage, save_folder)
    
    