from evaluator import (
    calculate_credibility,
    rank_papers
)


def evaluator_agent(papers):

    evaluated_papers = []

    for paper in papers:

        credibility = calculate_credibility(
            paper
        )

        paper["credibility"] = credibility

        evaluated_papers.append(paper)

    ranked = rank_papers(
        evaluated_papers
    )

    return ranked