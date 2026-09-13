from evaluator import (
    evaluate_papers,
    rank_papers,
    rank_under_recognized
)


def evaluator_agent(papers):

    # --------------------------------------------------------
    # Evaluate every retrieved paper
    # --------------------------------------------------------

    evaluated_papers = evaluate_papers(
        papers
    )

    # --------------------------------------------------------
    # Standard ranking
    # Highest research quality first
    # --------------------------------------------------------

    ranked_papers = rank_papers(
        evaluated_papers
    )

    # --------------------------------------------------------
    # Under-recognized research
    # Strong research quality + relatively low attention
    # --------------------------------------------------------

    under_recognized_papers = (
        rank_under_recognized(
            evaluated_papers
        )
    )

    return {
        "ranked_papers": ranked_papers,
        "under_recognized": under_recognized_papers
    }