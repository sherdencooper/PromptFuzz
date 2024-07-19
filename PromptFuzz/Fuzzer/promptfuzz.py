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
from gptfuzzer.llm import OpenAILLM, OpenAIEmbeddingLLM, LocalLLM, LocalVLLM
from PromptFuzz.utils import constants

import random
random.seed(100)
import logging
httpx_logger: logging.Logger = logging.getLogger("httpx")
# disable httpx logging
httpx_logger.setLevel(logging.WARNING)


def run_fuzzer(args):
        
    mutate_model = OpenAILLM(args.model_path, args.openai_key)
    # target_model = OpenAILLM(args.model_path, args.openai_key)
    target_model = LocalVLLM(args.target_model)
    # target_model = LocalLLM(args.target_model) # we suggest using LocalVLLM for better performance, however if you are facing difficulties in installing vllm, you can use LocalLLM instead
    
    if args.mode == 'hijacking':
        predictor = AccessGrantedPredictor()
    elif args.mode == 'extraction':
        predictor = MatchPredictor()
        
    save_path = f'./Results/{args.phase}/{args.mode}/{args.index}.csv' if not args.all_defenses else f'./Results/{args.phase}/{args.mode}/all_results.csv'    
    print("The save path is: ", save_path)
    # check if the directory exists
    if not os.path.exists(os.path.dirname(save_path)):
        os.makedirs(os.path.dirname(save_path))
    
    if args.phase == 'init':
        initial_seed_path = f'./Datasets/{args.mode}_robustness_dataset.jsonl'
    elif args.phase == 'focus':
        initial_seed_path = f'./Datasets/{args.mode}_focus_seed.jsonl'
    elif args.phase == 'evaluate':
        initial_seed_path = f'./Datasets/{args.mode}_evaluate_seed.jsonl'
        
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
        
        if args.mode == 'hijacking':
            weights = [0.2, 0.2, 0.2, 0.2, 0.2]
        elif args.mode == 'extraction':
            weights = [0.1, 0.1, 0.4, 0.2, 0.2]
        few_shot_examples = pd.read_csv(f'./Datasets/{args.mode}_evaluate_example.csv')
        embedding_model = OpenAIEmbeddingLLM("text-embedding-ada-002", args.openai_key)
        mutate_policy = MutateWeightedSamplingPolicy(
            mutator_list,
            weights=weights,
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
