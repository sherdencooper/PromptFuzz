# Running Scripts

## Preparation Stage

### Running Preparation Stage

To get the most potential attack seeds, run the preparation stage scripts first. Ensure the PHASE parameter is set to preparation. You can change the MODE parameter to hijacking or extraction to run different tasks.

```shell
nohup bash ./Scripts/promptfuzz_preparation_seed_evaluate.sh &
```

### Analysis Preparation Stage

After the preparation stage is finished, you will get these two files:

- `./Results/preparation/${MODE}/all_results.csv` # The attack results of all defenses
- `./Logs/preparation/${MODE}/all_defenses.log`    # The log file during the preparation stage

You can run the analysis script to get the focus attack seeds and the few-shot examples.

```shell
bash ./Scripts/analysis_preparation.sh
```

After running the analysis script, you will get these two files:

- `./Datasets/${MODE}/_focus_seeds.csv` # The focus attack seeds
- `./Datasets/${MODE}/_few_shot_example.csv` # The few-shot examples

## Focus Stage

### Running Focus Stage

After obtaining the focus attack seeds and the few-shot examples, you can run the focus stage scripts. In the script, ensure the PHASE parameter is set to focus. You can change the `MODE` parameter to `hijacking` or `extraction` to run the different tasks.

If you want to run the normal focus attack, you can run the following script:

```shell
nohup bash ./Scripts/promptfuzz_focus_attack.sh &
```

If you want to run the challenge focus attack, you can run the following script:

```shell
nohup bash ./Scripts/promptfuzz_challenge_defense.sh &
```

If you want to run the baseline comparison, use the following script. You can change the `BASELINE` parameter to `gcg` or `human_expert` to run different baselines in the second script.

```shell
# For GPTFuzzer
nohup bash ./Scripts/baseline_fuzzing.sh &

# For GCG & Human Expert & Initial Seed
nohup bash ./Scripts/baseline_static.sh &
```

### Analysis Focus Stage

After once the focus stage is finished, you will get these two kinds of results files:

- `./Results/focus/${MODE}/.../all_results.csv` # The attack results of **all defenses**, for `promptfuzz`, `gptfuzz`
- `./Results/init/${MODE}/.../*.csv`    # The attack results for **each defense**, for `human_expert`, `gcg`, `initial_seed`

You can run the analysis script to get uniform results and metrics. Specify the `METHOD` as `promptfuzz` `gptfuzz`, `human_expert`, `gcg` or `initial_seed` to call different functions. Also, you need to specify the target file or folder.

```shell
nohup bash ./Scripts/analysis_focus.sh &
```
