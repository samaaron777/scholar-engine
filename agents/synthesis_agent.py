def synthesis_agent(
    query,
    ranked_papers,
    reasoning_output
):

    summary = f"""
Research Topic:
{query}

Top Papers:
"""

    for paper in ranked_papers[:3]:

        summary += f"""

Title:
{paper['title']}

Credibility:
{paper['credibility']}

"""

    summary += "\nContradictions:\n"

    for item in reasoning_output["contradictions"]:

        summary += f"- {item}\n"

    return summary