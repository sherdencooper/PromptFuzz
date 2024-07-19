from openai import OpenAI
import tqdm
from datasets import load_dataset

# Set your OpenAI API key
api_key = 'YOUR_API_KEY'
client = OpenAI(api_key=api_key)

# Load MMLU dataset from Hugging Face
dataset = load_dataset("cais/mmlu", "all", split="validation")

# Prepare the dataset in the required format
mmlu_data = []
for item in dataset:
    mmlu_data.append({
        "question": item["question"],
        "choices": [f"A) {item['choices'][0]}", f"B) {item['choices'][1]}", f"C) {item['choices'][2]}", f"D) {item['choices'][3]}"],
        "answer": ["A", "B", "C", "D"][item["answer"]]
    })

# Zero-shot evaluation
def evaluate_zero_shot(data):
    correct = 0
    total = len(data)
    for i, item in enumerate(tqdm.tqdm(data, desc="Zero-shot Evaluation"), 1):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Question: {item['question']}\nChoices: {', '.join(item['choices'])}\nAnswer:"}
            ]
        )
        answer = response.choices[0].message.content.strip()
        if answer == item['answer']:
            correct += 1
        if i % 10 == 0:
            accuracy = correct / i
            print(f"Zero-shot accuracy after {i} questions: {accuracy:.2%}")
    
    accuracy = correct / total
    print(f"Zero-shot accuracy: {accuracy:.2%}")

# 5-shot evaluation
def evaluate_five_shot(data):
    correct = 0
    total = len(data)
    
    # Prepare the 5-shot examples
    five_shot_examples = [
        {"question": "What is the largest planet in our solar system?", "choices": ["A) Earth", "B) Mars", "C) Jupiter", "D) Saturn"], "answer": "C"},
        {"question": "Who wrote 'Pride and Prejudice'?", "choices": ["A) Mark Twain", "B) Jane Austen", "C) Charles Dickens", "D) J.K. Rowling"], "answer": "B"},
        {"question": "What is the boiling point of water?", "choices": ["A) 50°C", "B) 100°C", "C) 150°C", "D) 200°C"], "answer": "B"},
        {"question": "What is the powerhouse of the cell?", "choices": ["A) Nucleus", "B) Mitochondria", "C) Ribosome", "D) Endoplasmic Reticulum"], "answer": "B"},
        {"question": "What is the capital of Japan?", "choices": ["A) Seoul", "B) Beijing", "C) Tokyo", "D) Bangkok"], "answer": "C"},
    ]
    
    five_shot_prompt = ""
    for example in five_shot_examples:
        five_shot_prompt += f"Question: {example['question']}\nChoices: {', '.join(example['choices'])}\nAnswer: {example['answer']}\n\n"

    for i, item in enumerate(tqdm.tqdm(data, desc="5-shot Evaluation"), 1):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Answer the option that best answers the question. Give your answer in the format 'A', 'B', 'C', or 'D'."},
                {"role": "user", "content": five_shot_prompt + f"Question: {item['question']}\nChoices: {', '.join(item['choices'])}\nAnswer:"}
            ]
        )
        answer = response.choices[0].message.content.strip()
        if answer == item['answer']:
            correct += 1
        if i % 10 == 0:
            accuracy = correct / i
            print(f"5-shot accuracy after {i} questions: {accuracy:.2%}")
    
    accuracy = correct / total
    print(f"5-shot accuracy: {accuracy:.2%}")

# Evaluate both zero-shot and 5-shot
evaluate_five_shot(mmlu_data)
# evaluate_zero_shot(mmlu_data)

