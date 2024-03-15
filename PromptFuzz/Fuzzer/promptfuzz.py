import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import pandas as pd
import json
from gptfuzzer.fuzzer.selection import MCTSExploreSelectPolicy, RoundRobinSelectPolicy
from gptfuzzer.fuzzer.mutator import (
    MutateRandomSinglePolicy, NoMutatePolicy, OpenAIMutatorCrossOver, OpenAIMutatorExpand,
    OpenAIMutatorGenerateSimilar, OpenAIMutatorRephrase, OpenAIMutatorShorten)
from gptfuzzer.fuzzer import GPTFuzzer
from gptfuzzer.utils.predict import MatchPredictor, AccessGrantedPredictor
from gptfuzzer.llm import OpenAILLM
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
        
    save_path = f'./Results/{args.phase}/{args.mode}/{args.index}.csv'    
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
    
    mutate_policy = MutateRandomSinglePolicy([
            OpenAIMutatorCrossOver(mutate_model), 
            OpenAIMutatorExpand(mutate_model),
            OpenAIMutatorGenerateSimilar(mutate_model),
            OpenAIMutatorRephrase(mutate_model),
            OpenAIMutatorShorten(mutate_model)],
            concatentate=True,
        )
    select_policy = MCTSExploreSelectPolicy()
    
    if args.no_mutate:
        mutate_policy = NoMutatePolicy()
        args.energy = 1
        args.max_query = len(initial_seed)
        args.max_jailbreak = 9999999
        select_policy = RoundRobinSelectPolicy()
        
    if args.phase == 'evaluate':
        args.energy = 1
        args.max_jailbreak = 9999999
        args.max_query = len(initial_seed) * len(args.defenses) * 10
        select_policy = RoundRobinSelectPolicy()

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
    )

    fuzzer.run()
