def create_research_plan(query: str):

    plan = []

    query_lower = query.lower()

    if any(word in query_lower for word in [
        "research",
        "study",
        "scientific",
        "effect",
        "analysis"
    ]):
        plan.append("semantic_scholar")

    if any(word in query_lower for word in [
        "paper",
        "theory",
        "machine learning",
        "ai"
    ]):
        plan.append("arxiv")

    plan.append("memory_search")

    return plan