from services.retrieval_service import (
    semantic_scholar_search_structured
)

from tools import (
    arxiv,
    memory_search_tool,
    search_tool,
    wiki_tool
)


def retrieval_agent(query: str):

    results = {}

    
    
    # SEMANTIC SCHOLAR
    

    try:

        results["semantic_scholar"] = (
            semantic_scholar_search_structured(
                query
            )
        )

    except Exception as e:

        results["semantic_scholar"] = (
            str(e)
        )


    # ARXIV

    try:

        results["arxiv"] = (
            arxiv.run(query)
        )

    except Exception as e:

        results["arxiv"] = str(e)


    
    # VECTOR MEMORY
    

    try:

        results["memory"] = (
            memory_search_tool.run(
                query
            )
        )

    except Exception as e:

        results["memory"] = str(e)


    
    # WEB SEARCH
    

    try:

        results["web"] = (
            search_tool.run(query)
        )

    except Exception as e:

        results["web"] = str(e)


    
    # WIKIPEDIA
    

    try:

        results["wikipedia"] = (
            wiki_tool.run(query)
        )

    except Exception as e:

        results["wikipedia"] = str(e)

    return results