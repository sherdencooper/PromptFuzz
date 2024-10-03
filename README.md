# PromptFuzz: Harnessing Fuzzing Techniques for Robust Testing of Prompt Injection in LLMs

## Table of Contents

- [PromptFuzz: Harnessing Fuzzing Techniques for Robust Testing of Prompt Injection in LLMs](#promptfuzz-harnessing-fuzzing-techniques-for-robust-testing-of-prompt-injection-in-llms)
  - [Table of Contents](#table-of-contents)
  - [News](#news)
  - [Quick Start](#quick-start)
    - [Setup environment](#setup-environment)
    - [Datasets](#datasets)
    - [Set API key](#set-api-key)
    - [Fine-tuned Model](#fine-tuned-model)
    - [Running Focus Stage](#running-focus-stage)

## News

(2024/07/22) Congrats to our team for NO REASON!

## Quick Start

### Setup environment

```shell
conda create -n promptfuzz python=3.10
conda activate promptfuzz
pip install -r requirements.txt
```

### Datasets

We provide the datasets for preparation and focus stages, including the attack seeds, defense prompts, and few-shot examples. You can read the [Datasets](./Datasets/README.md) for more details, and the dataset names are as follows:

|Dataset Name| Stage |
|---|---|
|extraction/hijacking_preparation_defense.jsonl|Preparation|
|extraction/hijacking_preparation_seed.jsonl|Preparation|
|extraction/hijacking_focus_seed.jsonl|Focus|
|extraction/hijacking_few_shot_examples.csv|Focus|
|extraction/hijacking_focus_defense.jsonl|Focus|
|extraction/hijacking_focus_challenging_defense.jsonl|Focus|

You can use the following scripts to generate the focus attack seeds and the few-shot examples:

```shell
nohup bash ./Scripts/promptfuzz_preparation.sh &
bash ./Scripts/analysis_preparation.sh
```

### Set API key

You need to set the API key for the model you want to use. In PromptFuzz, the default model is gpt-3.5-turbo-0125. You can set your api_key in the [constants.py](./PromptFuzz/utils/constants.py).

```python
openai_key = 'your_openai_key'
```

### Fine-tuned Model

You can fine-tuned the model using the following scripts:

```shell
nohup bash ./Scripts/promptfuzz_finetune.sh &
```

You can read a detailed introduction about the fine-tuned dataset and the workflow of fine-tuning in the [Finetune](./Finetune/README.md).

### Running Focus Stage

You can run the focus attack, challenge focus attack, and baseline comparison using the following scripts:

```shell
# For focus attack
nohup bash ./Scripts/promptfuzz_focus_attack.sh &

# For challenge defense attack
nohup bash ./Scripts/promptfuzz_challenge_defense.sh &

# For baseline comparison
nohup bash ./Scripts/baseline_gptfuzzer.sh &
nohup bash ./Scripts/baseline_humanexpert_gcg.sh &
```

You can read the detailed introduction in the [Scripts](./Scripts/README.md).

## Citation
If you find this useful in your research, please consider citing:

```
@article{yu2024promptfuzz,
  title={PROMPTFUZZ: Harnessing Fuzzing Techniques for Robust Testing of Prompt Injection in LLMs},
  author={Yu, Jiahao and Shao, Yangguang and Miao, Hanwen and Shi, Junzheng and Xing, Xinyu},
  journal={arXiv preprint arXiv:2409.14729},
  year={2024}
}
```
