from simiir.user.query_generators.base import BaseQueryGenerator
from ifind.common.utils import get_given_queries

class ContextualExpansionQueryGenerator(BaseQueryGenerator):
    """
    Prepends or appends a few topic terms to make queries more focused.
    Uses user_context.topic.title and topic.description if available.
    """

    def __init__(self, stopword_file, query_file, user, background_file=[]):
        super().__init__(stopword_file, background_file=[])
        self.__query_filename = query_file
        self.__user = user

    def _topic_terms(self, user_context, n=3):
        title = getattr(user_context.topic, "title", "") or ""
        desc = getattr(user_context.topic, "description", "") or ""
        terms = (title + " " + desc).split()
        # keep most informative first n terms (simple heuristic)
        return " ".join(terms[:n])

    def generate_query_list(self, user_context) -> list[tuple[str, int]]:
        base_queries = get_given_queries(self.__query_filename, self.__user, user_context.topic.id, task_a2=False)
        topic_part = self._topic_terms(user_context, n=3)
        out = []
        for q, order in base_queries:
            if topic_part:
                new_q = f"{q} {topic_part}"
            else:
                new_q = q
            out.append((new_q, order))
        return out
