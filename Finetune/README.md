# Fine-tune LLM

## Composition of the dataset

Referring to the OpenAI's work([paper](https://arxiv.org/pdf/2404.13208)), we constructed a fine-tuned dataset containing the following components:

| Part  | Size|
| ---  | --- |
| Aligned Open-Domain Task   | 186 |
| Misaligned Open-Domain Task | 236 |
| Misaligned Closed-Domain Task | 125 |
| Prompt Extraction Task | 199 |
| Prompt Hijacking Task | 194 |
| Apaca GPT4 Task | 1000 |

## How to finetuned LLM ?

During the fine-tuning process, first, the dataset should be checked. Then, the fine-tuning task needs to be started. The fine-tuning task can be canceled and monitored. The specific changes are as follows:

```python
parser.add_argument("--work_stage", type=str, choices=['check', 'start', 'monitor', 'cancel', 'download'], default='monitor')
```

### Step 1: Check the dataset

```python
python ./Finetune/fine_tune.py --work_stage check
```

### Step 2: Start the fine-tuning task

```python
python ./Finetune/fine_tune.py --work_stage start
```

### Step 3: Monitor the fine-tuning task

You can monitor the fine-tuning task by running the following command. To monitor a specific task's progress, add the `--fine_tune_job_id` parameter.

```python
python ./Finetune/fine_tune.py --work_stage monitor
```

## Recommended Running by bash script

You can directly run the bash script to fine-tune the LLM model.

Fistly, you need to modify the `fine_tune.sh` file to set the `WORK_STAGE` parameter to `check`, `start`, `monitor`, `cancel`, or `download`.

Then, you can run the following command to fine-tune the LLM model.

```bash
bash ./Scripts/fine_tune.sh
```
