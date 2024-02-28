import sys
import os

# Add the path to the PromptFuzz folder to sys.path
sys.path.append(os.path.abspath('../PromptFuzz/'))
import json
import argparse
from PromptFuzz.Fuzzer.promptfuzz import run_fuzzer
from PromptFuzz.utils import constants

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fuzzing parameters')
    parser.add_argument('--index', type=int, default=0, help='The index of the target prompt')
    parser.add_argument('--phase', choices=['evaluate', 'focus', 'init'], default='init', help='The phase of the fuzzing process')
    parser.add_argument('--mode', choices=['hijacking', 'extraction'], default='hijacking', help='The mode of the fuzzing process')
    parser.add_argument('--openai_key', type=str, default=None, help='OpenAI API Key')
    parser.add_argument('--model_path', type=str, default='gpt-3.5-turbo-0125', help='target model path')
    parser.add_argument('--max_query', type=int, default=1000,
                        help='The maximum number of queries')
    parser.add_argument('--max_jailbreak', type=int,
                        default=999999, help='The maximum jailbreak number')
    parser.add_argument('--energy', type=int, default=1,
                        help='The energy of the fuzzing process')
    parser.add_argument("--no_mutate", type=bool, default=True)

    args = parser.parse_args()
    
    if args.openai_key is None:
        args.openai_key = constants.openai_key
        
    defense = f'./Datasets/{args.mode}_robustness_dataset.jsonl'
    # read the jsnol file
    with open(defense, 'r') as f:
        defenses = [json.loads(line) for line in f.readlines()]
    defenses = defenses[args.index]
    args.defenses = [defenses]
    
    if args.no_mutate:
        assert args.phase == 'init'
        
    run_fuzzer(args)