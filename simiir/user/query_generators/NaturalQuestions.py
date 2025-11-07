from simiir.user.query_generators.base import BaseQueryGenerator
from ifind.common.utils import get_given_queries
import random 
class NaturalQuestionGenerator(BaseQueryGenerator):
    """
    Briefly describe the core idea of your query generator!
    """

    def __init__(self, stopword_file, query_file, user, background_file=[]):
        super().__init__(stopword_file, background_file=[])
        self.__query_filename = query_file
        self.__user = user

    def generate_query_list(self, user_context) -> list[tuple[str, int]]:
        """
        Generates a list of queries for the given user context.
        Returns a list of tuples: (query_text, order_value)
        """
        # Lade bereits gegebene Queries aus der CSV
        return_queries: list[tuple[str, int]] = get_given_queries(
            self.__query_filename, self.__user, user_context.topic.id, task_a2=False
        )

        # Erstelle eine neue, automatisch generierte Frage basierend auf der letzten Query
        if return_queries:  # Prüfen, ob die Liste nicht leer ist
            new_query: tuple[str, int] = (self.create_question(return_queries[-1][0]), 0)
            return_queries.append(new_query)

        # Rückgabe der vollständigen Liste
        return return_queries


    def create_question(self, query: str) -> str:
        """
        Generates a natural language question from a query string by prepending a random prefix.
        """
        prefixes: list[str] = [
            "What is",
            "How to",
            "How would I",
            "Why is",
            "Where is",
        ]
        chosen_prefix: str = random.choice(prefixes)
        question_query: str = f"{chosen_prefix} {query.strip()}?"
        return question_query
        
