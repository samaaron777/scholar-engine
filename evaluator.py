from datetime import datetime


def calculate_credibility(paper):

    score = 0

    citations = paper.get("citationCount", 0)

    if citations > 5000:
        score += 0.4
    elif citations > 1000:
        score += 0.3
    elif citations > 100:
        score += 0.2
    else:
        score += 0.1

    year = paper.get("year", 2000)
    current_year = datetime.now().year

    if current_year - year <= 2:
        score += 0.3
    elif current_year - year <= 5:
        score += 0.2
    else:
        score += 0.1

    abstract = paper.get("abstract", "")

    if len(abstract) > 500:
        score += 0.3
    elif len(abstract) > 200:
        score += 0.2
    else:
        score += 0.1

    return round(min(score, 1.0), 2)


def rank_papers(papers):

    ranked = sorted(
        papers,
        key=lambda x: x.get("credibility", 0),
        reverse=True
    )

    return ranked