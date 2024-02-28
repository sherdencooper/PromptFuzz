import logging
import time
import csv

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .mutator import Mutator, MutatePolicy
    from .selection import SelectPolicy

from gptfuzzer.llm import LLM
from gptfuzzer.utils.template import synthesis_message
from gptfuzzer.utils.predict import Predictor
import warnings


class PromptNode:
    def __init__(self,
                 fuzzer: 'GPTFuzzer',
                 prompt: str,
                 response: str = None,
                 results: 'list[int]' = None,
                 parent: 'PromptNode' = None,
                 mutator: 'Mutator' = None):
        self.fuzzer: 'GPTFuzzer' = fuzzer
        self.prompt: str = prompt
        self.response: str = response
        self.results: 'list[int]' = results
        self.visited_num = 0

        self.parent: 'PromptNode' = parent
        self.mutator: 'Mutator' = mutator
        self.child: 'list[PromptNode]' = []
        self.level: int = 0 if parent is None else parent.level + 1

        self._index: int = None

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, index: int):
        self._index = index
        if self.parent is not None:
            self.parent.child.append(self)

    @property
    def num_jailbreak(self):
        return sum(self.results)

    @property
    def num_reject(self):
        return len(self.results) - sum(self.results)

    @property
    def num_query(self):
        return len(self.results)


class GPTFuzzer:
    def __init__(self,
                 defenses: 'list[dict]',
                 target: 'LLM',
                 predictor: 'Predictor',
                 initial_seed: 'list[str]',
                 mutate_policy: 'MutatePolicy',
                 select_policy: 'SelectPolicy',
                 max_query: int = -1,
                 max_jailbreak: int = -1,
                 max_reject: int = -1,
                 max_iteration: int = -1,
                 energy: int = 1,
                 result_file: str = None,
                 generate_in_batch: bool = False,
                 ):

        self.defenses: 'list[dict]' = defenses
        self.target: LLM = target
        self.predictor = predictor
        self.prompt_nodes: 'list[PromptNode]' = [
            PromptNode(self, prompt) for prompt in initial_seed
        ]
        self.initial_prompts_nodes = self.prompt_nodes.copy()

        for i, prompt_node in enumerate(self.prompt_nodes):
            prompt_node.index = i

        self.mutate_policy = mutate_policy
        self.select_policy = select_policy

        self.current_query: int = 0
        self.current_jailbreak: int = 0
        self.current_reject: int = 0
        self.current_iteration: int = 0

        self.max_query: int = max_query
        self.max_jailbreak: int = max_jailbreak
        self.max_reject: int = max_reject
        self.max_iteration: int = max_iteration

        self.energy: int = energy
        if result_file is None:
            result_file = f'results-{time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())}.csv'

        self.raw_fp = open(result_file, 'w', buffering=1)
        self.writter = csv.writer(self.raw_fp)
        self.writter.writerow(
            ['index', 'prompt', 'response', 'parent', 'results'])
        self.generate_in_batch = True
        self.setup()

    def setup(self):
        self.mutate_policy.fuzzer = self
        self.select_policy.fuzzer = self
        logging.basicConfig(
            level=logging.INFO, format='%(asctime)s %(message)s', datefmt='[%H:%M:%S]')

    def is_stop(self):
        checks = [
            ('max_query', 'current_query'),
            ('max_jailbreak', 'current_jailbreak'),
            ('max_reject', 'current_reject'),
            ('max_iteration', 'current_iteration'),
        ]
        return any(getattr(self, max_attr) != -1 and getattr(self, curr_attr) >= getattr(self, max_attr) for max_attr, curr_attr in checks)

    def run(self):
        logging.info("Fuzzing started!")
        try:
            while not self.is_stop():
                seed = self.select_policy.select()
                mutated_results = self.mutate_policy.mutate_single(seed)
                self.evaluate(mutated_results)
                self.update(mutated_results)
                self.log()
        except KeyboardInterrupt:
            logging.info("Fuzzing interrupted by user!")

        logging.info("Fuzzing finished!")
        self.raw_fp.close()

    def evaluate(self, prompt_nodes: 'list[PromptNode]'):
        # Initialize response and results as empty lists for each prompt node
        for prompt_node in prompt_nodes:
            prompt_node.response = []
            prompt_node.results = []
        
        messages = [prompt_node.prompt for prompt_node in prompt_nodes]
        
        for defense in self.defenses:
            # Generate responses in batch
            responses = self.target.generate_batch(messages, target=defense)

            # Batch predict for all responses
            predictions = self.predictor.predict(responses, defense['access_code'])
            
            # Append responses and results to prompt nodes
            for prompt_node, response, prediction in zip(prompt_nodes, responses, predictions):
                prompt_node.response.append(response)
                prompt_node.results.append(prediction)
            print(responses)

    def update(self, prompt_nodes: 'list[PromptNode]'):
        self.current_iteration += 1

        for prompt_node in prompt_nodes:
            if prompt_node.num_jailbreak > 0:
                prompt_node.index = len(self.prompt_nodes)
                self.prompt_nodes.append(prompt_node)
                self.writter.writerow([prompt_node.index, prompt_node.prompt,
                                       prompt_node.response, prompt_node.parent.index, prompt_node.results])

            self.current_jailbreak += prompt_node.num_jailbreak
            self.current_query += prompt_node.num_query
            self.current_reject += prompt_node.num_reject

        self.select_policy.update(prompt_nodes)

    def log(self):
        logging.info(
            f"Iteration {self.current_iteration}: {self.current_jailbreak} jailbreaks, {self.current_reject} rejects, {self.current_query} queries")
