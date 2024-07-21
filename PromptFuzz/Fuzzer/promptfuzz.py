import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import pandas as pd
import json
from gptfuzzer.fuzzer.selection import MCTSExploreSelectPolicy, RoundRobinSelectPolicy
from gptfuzzer.fuzzer.mutator import (
    MutateRandomSinglePolicy, NoMutatePolicy, MutateWeightedSamplingPolicy, OpenAIMutatorCrossOver, OpenAIMutatorExpand,
    OpenAIMutatorGenerateSimilar, OpenAIMutatorRephrase, OpenAIMutatorShorten)
from gptfuzzer.fuzzer import GPTFuzzer
from gptfuzzer.utils.predict import MatchPredictor, AccessGrantedPredictor
from gptfuzzer.llm import OpenAILLM, OpenAIEmbeddingLLM
from PromptFuzz.utils import constants

import random
random.seed(100)
import logging
httpx_logger: logging.Logger = logging.getLogger("httpx")
# disable httpx logging
httpx_logger.setLevel(logging.WARNING)


def run_fuzzer(args):
        
    mutate_model = OpenAILLM(args.model_path, args.openai_key)
    target_model = OpenAILLM(args.model_path, args.openai_key)
    
    if args.mode == 'hijacking':
        predictor = AccessGrantedPredictor()
    elif args.mode == 'extraction':
        predictor = MatchPredictor()
    
    if args.baseline == 'humanexpert' or args.baseline == 'gcg':
        save_path = f'./Results/{args.phase}/{args.mode}/baseline/{args.baseline}/{args.index}.csv' if not args.all_defenses else f'./Results/{args.phase}/{args.mode}/baseline/{args.baseline}/all_results.csv'    
    else:
        save_path = f'./Results/{args.phase}/{args.mode}/{args.index}.csv' if not args.all_defenses else f'./Results/{args.phase}/{args.mode}/all_results.csv'    
    
    print("The save path is: ", save_path)

    # check if the directory exists
    if not os.path.exists(os.path.dirname(save_path)):
        os.makedirs(os.path.dirname(save_path))
    
    # load the defense prompt
    if args.phase == 'init':
        if args.baseline == 'humanexpert':
            defense = f'./Datasets/{args.mode}_humanexpert_baseline.jsonl'
        elif args.baseline == 'gcg': 
            defense = f'./Datasets/{args.mode}_gcg_baseline.jsonl'
        defense = f'./Datasets/{args.mode}_robustness_dataset.jsonl'
    elif args.phase == 'focus':
        defense = f'./Datasets/{args.mode}_focus_defense.jsonl'
    elif args.phase == 'preparation':
        defense = f'./Datasets/{args.mode}_preparation_defense.jsonl'
    
    with open(defense, 'r') as f:
        defenses = [json.loads(line) for line in f.readlines()]
        
    if args.all_defenses:
        defenses = defenses
    else:
        defenses = defenses[args.index]
        defenses = [defenses]
    
    if args.no_mutate:
        assert args.phase == 'init'

    # load the initial seed
    if args.phase == 'init':
        initial_seed_path = f'./Datasets/{args.mode}_robustness_dataset.jsonl'
    elif args.phase == 'focus':
        initial_seed_path = f'./Datasets/{args.mode}_focus_seed.jsonl'
    elif args.phase == 'preparation':
        initial_seed_path = f'./Datasets/{args.mode}_preparation_seed.jsonl'
        
    with open(initial_seed_path, 'r') as f:
        initial_seed = [json.loads(line)['attack'] for line in f.readlines()]
    
    mutator_list = [
            OpenAIMutatorCrossOver(mutate_model), 
            OpenAIMutatorExpand(mutate_model),
            OpenAIMutatorGenerateSimilar(mutate_model),
            OpenAIMutatorRephrase(mutate_model),
            OpenAIMutatorShorten(mutate_model)
            ]
    
    mutate_policy = MutateRandomSinglePolicy(
            mutator_list,
            concatentate=args.concatenate,
        )
    select_policy = MCTSExploreSelectPolicy()
    
    if args.no_mutate:
        mutate_policy = NoMutatePolicy()
        args.energy = 1
        args.max_query = len(initial_seed)
        select_policy = RoundRobinSelectPolicy()
        
    if args.phase == 'evaluate':
        args.energy = 1
        args.max_query = len(initial_seed) * len(args.defenses) * 10
        select_policy = RoundRobinSelectPolicy()
        
    if args.phase == 'focus':
        args.energy = 5
        args.max_query =  len(args.defenses) * 1000
        select_policy = MCTSExploreSelectPolicy()
        
        few_shot_examples = pd.read_csv(f'./Datasets/{args.mode}_evaluate_example.csv')
        embedding_model = OpenAIEmbeddingLLM("text-embedding-ada-002", args.openai_key)
        mutate_policy = MutateWeightedSamplingPolicy(
            mutator_list,
            weights=args.weights,
            few_shot=args.few_shot,
            few_shot_num=args.few_shot_num,
            few_shot_file=few_shot_examples,
            concatentate=args.concatenate,
            retrieval_method=args.retrieval_method,
            cluster_num=args.cluster_num,
            embedding_model=embedding_model,
        )
        
    update_pool = True if args.phase == 'focus' else False

    fuzzer = GPTFuzzer(
        defenses=args.defenses,
        target=target_model,
        predictor=predictor,
        initial_seed=initial_seed,
        result_file=save_path,
        mutate_policy=mutate_policy,
        select_policy=select_policy,
        energy=args.energy,
        max_jailbreak=args.max_jailbreak,
        max_query=args.max_query,
        update_pool=update_pool,
        dynamic_allocate=args.dynamic_allocate,
        threshold_coefficient=args.threshold_coefficient
    )

    fuzzer.run()
