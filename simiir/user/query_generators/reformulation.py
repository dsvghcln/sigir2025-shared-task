from simiir.user.query_generators.base import BaseQueryGenerator
from ifind.common.utils import get_given_queries
import random

class ReformulationQueryGenerator(BaseQueryGenerator):
    """
    Reformulates given queries using simple template patterns.
    """

    def __init__(self, stopword_file, query_file, user, background_file=[]):
        super().__init__(stopword_file, background_file=[])
        self.__query_filename = query_file
        self.__user = user
        self.templates = [
            "information about {}",
            "research on {}",
            "latest studies about {}",
            "overview of {}",
            "how to understand {}",
        ]

    def generate_query_list(self, user_context) -> list[tuple[str, int]]:
        base_queries = get_given_queries(self.__query_filename, self.__user, user_context.topic.id, task_a2=False)
        out = []
        for q, order in base_queries:
            tpl = random.choice(self.templates)
            new_q = tpl.format(q.strip())
            out.append((new_q, order))
        return out
