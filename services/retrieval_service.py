import requests

from evaluator import (
    calculate_credibility,
    rank_papers
)

from vector_store import (
    add_to_vector_store
)


# SEMANTIC SCHOLAR STRUCTURED SEARCH

def semantic_scholar_search_structured(
    query: str
):

    url = (
        "https://api.semanticscholar.org/"
        "graph/v1/paper/search"
    )

    params = {
        "query": query,
        "limit": 10,
        "fields": (
            "title,"
            "authors,"
            "year,"
            "citationCount,"
            "url,"
            "abstract"
        )
    }

    response = requests.get(
        url,
        params=params
    )

    if response.status_code != 200:
        return []

    data = response.json()

    structured_papers = []

    for paper in data.get("data", []):

        title = paper.get(
            "title",
            "No title"
        )

        year = paper.get(
            "year",
            2000
        )

        citations = paper.get(
            "citationCount",
            0
        )

        abstract = paper.get(
            "abstract",
            "No abstract available"
        )

        paper_url = paper.get(
            "url",
            "No URL"
        )

        authors = [
            author["name"]
            for author in paper.get(
                "authors",
                []
            )
        ]

        credibility = (
            calculate_credibility(
                paper
            )
        )

        structured_papers.append(
            {
                "title": title,
                "authors": authors,
                "year": year,
                "citationCount": citations,
                "abstract": abstract,
                "url": paper_url,
                "credibility": credibility,
                "source_type": "Semantic Scholar"
            }
        )

        # Store in vector DB

        add_to_vector_store(
            text=f"{title}\n{abstract}",
            metadata={
                "title": title,
                "year": year,
                "credibility": credibility,
                "url": paper_url
            }
        )

    ranked_papers = rank_papers(
        structured_papers
    )

    return ranked_papers[:5]