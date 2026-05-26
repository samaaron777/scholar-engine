from langchain_community.tools import (
    WikipediaQueryRun,
    DuckDuckGoSearchRun,
    ArxivQueryRun
)

from langchain_community.utilities import (
    WikipediaAPIWrapper
)

from langchain.tools import Tool

from datetime import datetime

from vector_store import (
    search_vector_store
)

from services.retrieval_service import (
    semantic_scholar_search_structured
)

# SAVE TOOL


def save_to_txt(data: str):

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    with open(
        "outputs/research.txt",
        "a",
        encoding="utf-8"
    ) as f:

        f.write(
            f"\n--- {timestamp} ---\n{data}\n"
        )

    return "Saved"


save_tool = Tool(
    name="save_text",
    func=save_to_txt,
    description="Save research output to file."
)


# WEB SEARCH TOOL

search = DuckDuckGoSearchRun()

search_tool = Tool(
    name="search",
    func=search.run,
    description="Search the web for supplemental information."
)


# WIKIPEDIA TOOL


wiki = WikipediaQueryRun(
    api_wrapper=WikipediaAPIWrapper(
        top_k_results=2
    )
)

wiki_tool = wiki


# ARXIV TOOL

arxiv = ArxivQueryRun()


# SEMANTIC SCHOLAR TOOL

def semantic_scholar_search(
    query: str
):

    papers = (
        semantic_scholar_search_structured(
            query
        )
    )

    formatted_output = []

    for paper in papers:

        formatted_output.append(
            f"""
Title: {paper['title']}

Authors: {", ".join(paper['authors'])}

Year: {paper['year']}

Citation Count:
{paper['citationCount']}

Credibility Score:
{paper['credibility']}

Abstract:
{paper['abstract']}

URL:
{paper['url']}
"""
        )

    return "\n\n".join(
        formatted_output
    )


semantic_scholar_tool = Tool(
    name="semantic_scholar_search",
    func=semantic_scholar_search,
    description=(
        "Search Semantic Scholar for "
        "high-quality academic papers."
    )
)

# MEMORY SEARCH TOOL

def memory_search(query: str):

    results = search_vector_store(
        query
    )

    formatted = []

    for result in results:

        formatted.append(
            f"""
Title:
{result.metadata.get('title')}

Year:
{result.metadata.get('year')}

Credibility:
{result.metadata.get('credibility')}

URL:
{result.metadata.get('url')}

Content:
{result.page_content}
"""
        )

    return "\n\n".join(formatted)


memory_search_tool = Tool(
    name="memory_search",
    func=memory_search,
    description=(
        "Search previously stored "
        "research papers from vector memory."
    )
)