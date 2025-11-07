from simiir.user.query_generators.base import BaseQueryGenerator
from ifind.common.utils import get_given_queries

class SummarizationLLMQueryGenerator(BaseQueryGenerator):
    """
    Simulates summarization by concatenating previous queries and producing a focused 'summarized' query.
    Ensures that at least one valid query is always returned for Terrier.
    """

    def __init__(self, stopword_file, query_file, user, background_file=[]):
        super().__init__(stopword_file, background_file=[])
        self.__query_filename = query_file
        self.__user = user

    def generate_query_list(self, user_context) -> list[tuple[str, int]]:
        # Load previously issued queries
        base_queries = get_given_queries(
            self.__query_filename,
            self.__user,
            user_context.topic.id,
            task_a2=False
        )

        # Safety check: if base_queries is empty, provide a fallback query
        if not base_queries:
            return [("default safe query", 0)]

        # Combine previous queries into a single focused summary
        combined_short = " ".join([q.strip() for q, _ in base_queries if q.strip()])

        # If combined_short is empty (all previous queries were blank), fallback
       if not base_queries:
        return [("default safe query", 0)]

    combined_short = " ".join([q.strip() for q, _ in base_queries if q.strip()])
    if not combined_short:
        combined_short = "default safe query"

    summarized = f"Focused summary query: {combined_short}".strip()
    if not summarized:
        summarized = "default safe query"

        # Append summarized query at the end
        out = base_queries.copy()
        out.append((summarized, len(out)))

        return out
