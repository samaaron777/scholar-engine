from reasoning import (
    detect_contradictions
)


def reasoning_agent(papers):

    contradictions = (
        detect_contradictions(papers)
    )

    return {
        "contradictions": contradictions
    }