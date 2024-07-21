# PromptFuzz

# 1 Datasets

## **1.1 Preparation phase**

- hijacking_evaluate_defense.jsonl
- hijacking_evaluate_seed.jsonl

## 1.2 Focus phase

- hijacking_focus_challenging_defense.jsonl
- hijacking_focus_defense.jsonl
- hijacking_focus_seed.jsonl
- gcg_evaluate.jsonl
- lmi_evaluate.jsonl
- final_all_finetune_dataset.jsonl

# 2 Analysis Scripts

## 2.1 **Preparation phase**

Get data for the focus stage during preparation phase:

- In the PREPARE phase, on the results of the '`hijacking_evaluate_seed`' attack on '`hijacking_evaluate_defense`', based on the ASR to the attack prompts and then sampling them based on Top 40

    ```bash
    python get_attack_ranking.py
    python sample_top40_focus_seed.py
    ```

- Sample 10 attack prompts on each mutator as example dataset. at the same time, you can analyze the mutator's mutation in each attack prompt by '`get_mutator_distribution`'. Distribution of the mutator in each attack prompt mutation

    ```bash
    python sample_example_by_mutator.py
    
    python get_mutator_distribution.py
    ```


## 2.2 Focus phase

Get challenging data:

```bash
python get_focus_challenging_defense.py
```

Analysis of results:

- Access to harmonized formatting forms.

    ```markdown
    index,prompt,response,parent,results,mutation,query
    ->
    AttackID,AttackSuccessNum,AttackSuccessRate,ParentAttackID,AttackPrompt
    ```

    ```bash
    python get_uniform_result.py
    ```

- Aggregatting multiple csv results into one file.

    ```bash
    python aggregate_csv_results.py
    ```

- Getting the BestASR, ESR, Coverage metrics corresponding to the **initial seeds** method.

    ```bash
    python get_initial_baseline_metric.py
    ```

- Getting the BestASR, ESR, Coverage metrics corresponding to PromptFuzz, GPTFuzz, LMI, GCG methods.

    ```bash
    python get_baseline_metric.py
    ```

    In particular, for experiments with LMI and GCG methods, as well as Challenging Defense experiments, you need to execute python aggregate_csv_results.py first, and then enter the path to the aggregated results before executing this command.

- Getting Iteration Data.

    ```bash
    get_iteration_results.py
    ```
    

# 3 Run Script

## 3.1 Baseline methods

```bash
# LMI
bash lmi_attack_single_all.sh

# GCG
bash gcg_attack_single_all.sh

# GPTFuzzer-Injection
bash focus_attack_gptfuzzer.sh

# PromptFuzz
bash focus_attack.sh
```

## 3.2 Fine-tune GPT

```bash
bash fine_tune.sh
```

## 3.3 Attack Challenging Defense

```bash
# Base model
bash focus_attack_single_challenging_base.sh

# Finetuned model
bash focus_attack_single_challenging_finetuned.sh
```