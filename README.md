# Scripts
## GPTFuzzer baseline
focus_attack_GPTFuzzer.sh 
_usage_: bash Scripts/focus_attack_GPTFuzzer.sh
## select attack seeds/get ASR of seeds
init_evaluation.sh 
_usage_: bash Scripts/init_evaluation.sh(each defense has a csv file)
seed_evaluate.sh
_usage_: bash Scripts/seed_evaluate.sh(all defenses in one csv file)
## attack all 100%DSR defenses
focus_attack_defense100.sh
_usage_: bash Scripts/focus_attack_defense100.sh defense100_index.txt
## focus to attack one defense until success
focus_attack_single.sh
_usage_: bash Scripts/focus_attack_single.sh index
## crossover attack on all defenses
focus_attack.sh 
_usage_: bash Scripts/focus_attack.sh
## repeat the process
focus_attack_many_times.sh 
_usage_: bash Scripts/focus_attack_many_times.sh
# Datasets
## prepare phase 
extraction_evaluate_seed.jsonl
extraction_evaluate_defense.jsonl
## focus phase
**focus seeds selected from prepare phase**
extraction_focus_seed.jsonl
extraction_focus_defense.jsonl
**random focus seed**
extraction_random_focus_seed.jsonl
## LMI attack prompts
extraction_LMI_seed.jsonl
## GCG attack_prompts
extraction_GCG_seed.jsonl
# Analysis
## prepare phase: calculate ASR;get focus seeds
evaluate_analyze.py
## prepare phase: get mutators' weights
evaluate_mutator_analyze.py
## focus phase: caluculate ASR
focus_analyze.py
## get all 100%DSR defenses
get_defense100_from_focus.py
## get origin of each successful mutation
focus_analyze_find_origin.py
## calculate consumed tokens
token_consumed_analyze_defense100.sh #redirect
focus_analyze_defense100.py #get the consumed tokens to attack each defense
focus_statis_defense100.py #get mean and std
	

	
	

               