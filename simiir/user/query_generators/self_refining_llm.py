from simiir.user.query_generators.base import BaseQueryGenerator
from ifind.common.utils import get_given_queries

class SelfRefiningLLMQueryGenerator(BaseQueryGenerator):
    """
    Simulates iterative LLM refinement: each new query references the previous one for refinement.
    """

    def __init__(self, stopword_file, query_file, user, background_file=[]):
        super().__init__(stopword_file, background_file=[])
        self.__query_filename = query_file
        self.__user = user

    def generate_query_list(self, user_context) -> list[tuple[str, int]]:
        base_queries = get_given_queries(self.__query_filename, self.__user, user_context.topic.id, task_a2=False)
        refined = []
        prev = None
        for idx, (q, order) in enumerate(base_queries):
            if prev is None:
                new_q = f"{q}"
            else:
                new_q = f"Refine based on previous '{prev}': {q}"
            refined.append((new_q, order))
            prev = new_q
        return refined
