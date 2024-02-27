import os
import sys
os.environ['CUDA_VISIBLE_DEVICES'] = '0,1'  # for debugging

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from fastchat.model import add_model_args
import argparse
import pandas as pd
from gptfuzzer.fuzzer.selection import MCTSExploreSelectPolicy
from gptfuzzer.fuzzer.mutator import (
    MutateRandomSinglePolicy, OpenAIMutatorCrossOver, OpenAIMutatorExpand,
    OpenAIMutatorGenerateSimilar, OpenAIMutatorRephrase, OpenAIMutatorShorten)
from gptfuzzer.fuzzer import GPTFuzzer
from gptfuzzer.llm import OpenAILLM, LocalVLLM, LocalLLM, PaLM2LLM, ClaudeLLM
from PromptFuzz.utils import constants

import random
random.seed(100)
import logging
httpx_logger: logging.Logger = logging.getLogger("httpx")
# disable httpx logging
httpx_logger.setLevel(logging.WARNING)


def run_fuzzer(args):
    
    target = f'./Datasets/{args.mode}_{args.phase}.jsonl'
    # read the dataset
    df = pd.read_json(target, lines=True)
    
    openai_model = OpenAILLM(args.model_path, args.openai_key)

    save_path = f'./Results/{args.phase}/{args.mode}'
    if args.add_eos:
        save_path = f'./Results/{args.target_model}/GPTFuzzer_eos/{args.index}.csv'
    
    print("The save path is: ", save_path)

    fuzzer = GPTFuzzer(
        questions=questions,
        target=openai_model,
        predictor=roberta_model,
        initial_seed=initial_seed,
        mutate_policy=MutateRandomSinglePolicy([
            OpenAIMutatorCrossOver(openai_model), 
            OpenAIMutatorExpand(openai_model),
            OpenAIMutatorGenerateSimilar(openai_model),
            OpenAIMutatorRephrase(openai_model),
            OpenAIMutatorShorten(openai_model)],
            concatentate=True,
        ),
        select_policy=MCTSExploreSelectPolicy(),
        energy=args.energy,
        max_jailbreak=args.max_jailbreak,
        max_query=args.max_query,
        generate_in_batch=False,
    )

    fuzzer.run()



