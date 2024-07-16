import json
import tiktoken # for token counting
import argparse
import numpy as np
from openai import OpenAI
from collections import defaultdict


encoding = tiktoken.get_encoding("cl100k_base")

def dataset_check(dataset):
    # Format error checks
    format_errors = defaultdict(int)

    for ex in dataset:
        if not isinstance(ex, dict):
            format_errors["data_type"] += 1
            continue
            
        messages = ex.get("messages", None)
        if not messages:
            format_errors["missing_messages_list"] += 1
            continue
            
        for message in messages:
            if "role" not in message or "content" not in message:
                format_errors["message_missing_key"] += 1
            
            if any(k not in ("role", "content", "name", "function_call", "weight") for k in message):
                format_errors["message_unrecognized_key"] += 1
            
            if message.get("role", None) not in ("system", "user", "assistant", "function"):
                format_errors["unrecognized_role"] += 1
                
            content = message.get("content", None)
            function_call = message.get("function_call", None)
            
            if (not content and not function_call) or not isinstance(content, str):
                format_errors["missing_content"] += 1
        
        if not any(message.get("role", None) == "assistant" for message in messages):
            format_errors["example_missing_assistant_message"] += 1

    if format_errors:
        print("Found errors:")
        for k, v in format_errors.items():
            print(f"{k}: {v}")
            return False
    else:
        print("No errors found")
        return True

def num_tokens_from_messages(messages, tokens_per_message=3, tokens_per_name=1):
    num_tokens = 0
    allowed_special_tokens = {'', '<|endoftext|>'}  # 添加你想允许的特殊标记
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            if value or key == "name":  # 只有当value存在或者key是"name"时才编码
                num_tokens += len(encoding.encode(value, allowed_special=allowed_special_tokens))
    num_tokens += 3
    return num_tokens

def num_assistant_tokens_from_messages(messages):
    num_tokens = 0
    for message in messages:
        if message["role"] == "assistant":
            num_tokens += len(encoding.encode(message["content"]))
    return num_tokens

def print_distribution(values, name):
    print(f"\n#### Distribution of {name}:")
    print(f"min / max: {min(values)}, {max(values)}")
    print(f"mean / median: {np.mean(values)}, {np.median(values)}")
    print(f"p5 / p95: {np.quantile(values, 0.1)}, {np.quantile(values, 0.9)}")

def token_counts(dataset):
    # Warnings and tokens counts
    n_missing_system = 0
    n_missing_user = 0
    n_messages = []
    convo_lens = []
    assistant_message_lens = []

    for ex in dataset:
        messages = ex["messages"]
        if not any(message["role"] == "system" for message in messages):
            n_missing_system += 1
        if not any(message["role"] == "user" for message in messages):
            n_missing_user += 1
        n_messages.append(len(messages))
        convo_lens.append(num_tokens_from_messages(messages))
        assistant_message_lens.append(num_assistant_tokens_from_messages(messages))
        
    print("Num examples missing system message:", n_missing_system)
    print("Num examples missing user message:", n_missing_user)
    print_distribution(n_messages, "num_messages_per_example")
    print_distribution(convo_lens, "num_total_tokens_per_example")
    print_distribution(assistant_message_lens, "num_assistant_tokens_per_example")
    n_too_long = sum(l > 4096 for l in convo_lens)
    print(f"\n{n_too_long} examples may be over the 4096 token limit, they will be truncated during fine-tuning")

def main(args):
    # Data loading
    with open(args.data_path, 'r', encoding='utf-8') as f:
        dataset = [json.loads(line) for line in f]
    
     # Fine tuning
    client = OpenAI(
        api_key='APIKEY',
    )

    if args.work_stage == 'check':
        print("Num examples:", len(dataset))
        print("First example:")
        for message in dataset[0]["messages"]:
            print(message)

        # Data validation
        if dataset_check(dataset):
            print("Validation check passed")
        else:
            print("Validation check failed")
            return

        # Token counting
        token_counts(dataset)

    elif args.work_stage == 'start':
        response = client.files.create(
            file=open(f"{args.data_path}", "rb"),
            purpose="fine-tune"
        )

        file_id = response.id
        print(f"File uploaded successfully with ID: {file_id}")
        hyperparameters = {
            "n_epochs": 1  # 设置训练轮次为1
        }
        fine_tune_job = client.fine_tuning.jobs.create(
            training_file=file_id, 
            model="gpt-3.5-turbo",
        )
        print(f"Fine-tuning job created successfully: {fine_tune_job.id}")

        job_status = client.fine_tuning.jobs.retrieve(fine_tune_job.id)
        print(job_status)
        
    elif args.work_stage == 'monitor':
        # Monitor fine-tuning job
        job_status = client.fine_tuning.jobs.retrieve(args.fine_tune_job_id)
        print(job_status)

        # Show all
        all_jobs = client.fine_tuning.jobs.list()

        for job in all_jobs.data:
           print(f"Job ID: {job.id}, Model: {job.model}, Created At: {job.created_at}, Status: {job.status}")
        
    elif args.work_stage == 'cancel':
        # Delete fine-tuning job
        cancel_response = client.fine_tuning.jobs.cancel(args.fine_tune_job_id)
        print("Fine-tuning job cancelled successfully.\n\n", cancel_response)


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-path", type=str, default="./Datasets/fine_tune/final_all_finetune_dataset.jsonl")
    parser.add_argument("--fine-tune-job-id", type=str, default="JOBID")
    parser.add_argument("--work_stage", type=str, choices=['check', 'start', 'monitor', 'cancel', 'download'], default='monitor')
    
    args = parser.parse_args()
    
    main(args)