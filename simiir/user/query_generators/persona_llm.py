from simiir.user.query_generators.base import BaseQueryGenerator
from ifind.common.utils import get_given_queries
import random

class PersonaBasedLLMQueryGenerator(BaseQueryGenerator):
    """
    Simulates an LLM persona by prepending persona prompts (medical student, journalist, patient).
    """

    def __init__(self, stopword_file, query_file, user, background_file=[]):
        super().__init__(stopword_file, background_file=[])
        self.__query_filename = query_file
        self.__user = user
        self.personas = [
            "As a medical student, look for",
            "As a health journalist, investigate",
            "As a patient, ask about",
            "As a policymaker, evaluate",
        ]

    def generate_query_list(self, user_context) -> list[tuple[str, int]]:
        base_queries = get_given_queries(self.__query_filename, self.__user, user_context.topic.id, task_a2=False)
        persona = random.choice(self.personas)
        out = []
        for q, order in base_queries:
            new_q = f"{persona} {q}"
            out.append((new_q, order))
        return out
