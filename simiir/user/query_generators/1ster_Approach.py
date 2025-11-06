from simiir.user.query_generators.base import BaseQueryGenerator
from ifind.common.utils import get_given_queries
import random

class SecondApproachGenerator(BaseQueryGenerator):
    """
    Rule-based query generator for the second approach.
    """

    def __init__(self, stopword_file, query_file, user, background_file=[]):
        super().__init__(stopword_file, background_file=[])
        self.__query_filename = query_file
        self.__user = user

    def generate_query_list(self, user_context) -> list[tuple[str, int]]:
        return_queries: list[tuple[str, int]] = get_given_queries(
            self.__query_filename, self.__user, user_context.topic.id, task_a2=False
        )

        if return_queries:
            new_query: tuple[str, int] = (self.create_question(return_queries[-1][0]), 0)
            return_queries.append(new_query)

        return return_queries

    def create_question(self, query: str) -> str:
        prefixes = ["How can I", "What are", "Explain", "Give me", "List"]
        return f"{random.choice(prefixes)} {query.strip()}?"
