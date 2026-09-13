from tools import (
    semantic_scholar_tool,
    arxiv,
    memory_search_tool,
    search_tool,
    wiki_tool
)


def retrieval_agent(query: str):

    results = {}

    lower_query = query.lower()

    
    
    # ACADEMIC PRIORITY
    

    academic_keywords = [
        "study",
        "research",
        "effect",
        "clinical",
        "scientific",
        "evidence",
        "analysis",
        "meta-analysis",
        "experiment"
    ]


    is_academic = any(
        keyword in lower_query
        for keyword in academic_keywords
    )


    
    
    # ACADEMIC RETRIEVAL
    

    if is_academic:

        try:
            results["semantic_scholar"] = (
                semantic_scholar_tool.run(query)
            )
        except Exception as e:
            results["semantic_scholar"] = str(e)

        try:
            results["arxiv"] = (
                arxiv.run(query)
            )
        except Exception as e:
            results["arxiv"] = str(e)

    
    
    # GENERAL RETRIEVAL
    

    else:

        try:
            results["wikipedia"] = (
                wiki_tool.run(query)
            )
        except Exception as e:
            results["wikipedia"] = str(e)

        try:
            results["web"] = (
                search_tool.run(query)
            )
        except Exception as e:
            results["web"] = str(e)


    
    
    # MEMORY SEARCH
    

    try:
        results["memory"] = (
            memory_search_tool.run(query)
        )
    except Exception as e:
        results["memory"] = str(e)


    
    
    # SUPPLEMENTAL SEARCH
    

    try:
        results["web"] = (
            search_tool.run(query)
        )
    except Exception as e:
        results["web"] = str(e)


    return results