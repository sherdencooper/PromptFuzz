import argparse
from fastchat.model import add_model_args
from PromptFuzz.Fuzzer.promptfuzz import run_fuzzer
from PromptFuzz.utils import constants

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fuzzing parameters')
    parser.add_argument('--index', type=int, default=0, help='The index of the target prompt')
    parser.add_argument('--phase', choices=['evaluate', 'focus'], default='test', help='The phase of the fuzzing process')
    parser.add_argument('--mode', choices=['hijack', 'extraction'], default='hijack', help='The mode of the fuzzing process')
    parser.add_argument('--openai_key', type=str, default=None, help='OpenAI API Key')
    parser.add_argument('--model_path', type=str, default='gpt-3.5-turbo-0125', help='target model path')
    parser.add_argument('--max_query', type=int, default=1000,
                        help='The maximum number of queries')
    parser.add_argument('--max_jailbreak', type=int,
                        default=1, help='The maximum jailbreak number')
    parser.add_argument('--energy', type=int, default=1,
                        help='The energy of the fuzzing process')
    parser.add_argument('--seed_selection_strategy', type=str,
                        default='round_robin', help='The seed selection strategy')
    parser.add_argument("--max-new-tokens", type=int, default=512)
    add_model_args(parser)

    args = parser.parse_args()
    
    if args.openai_key is None:
        args.openai_key = constants.openai_key
    run_fuzzer(args)