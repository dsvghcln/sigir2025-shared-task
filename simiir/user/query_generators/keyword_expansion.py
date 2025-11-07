from simiir.user.query_generators.base import BaseQueryGenerator
from ifind.common.utils import get_given_queries

class KeywordExpansionQueryGenerator(BaseQueryGenerator):
    """
    Expands given queries using a small static synonym dictionary.
    """

    def __init__(self, stopword_file, query_file, user, background_file=[]):
        super().__init__(stopword_file, background_file=[])
        self.__query_filename = query_file
        self.__user = user

        # small expansion dictionary (extend as needed)
        self.synonyms = {
            "disease": ["illness", "condition"],
            "treatment": ["therapy", "medication"],
            "effect": ["impact", "influence"],
            "risk": ["hazard", "danger"],
        }

    def generate_query_list(self, user_context) -> list[tuple[str, int]]:
        base_queries = get_given_queries(self.__query_filename, self.__user, user_context.topic.id, task_a2=False)
        expanded = []
        for q, order in base_queries:
            additions = []
            q_lower = q.lower()
            for k, syns in self.synonyms.items():
                if k in q_lower:
                    additions.extend(syns)
            if additions:
                new_q = f"{q} {' '.join(additions)}"
            else:
                new_q = q
            expanded.append((new_q, order))
        return expanded
