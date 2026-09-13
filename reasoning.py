def detect_contradictions(papers):

    contradictions = []

    for paper in papers:

        abstract = (
            paper.get(
                "abstract",
                ""
            ).lower()
        )

        if (
            "however" in abstract
            or "limited" in abstract
            or "conflicting" in abstract
        ):

            contradictions.append(
                {
                    "title": paper.get(
                        "title"
                    ),
                    "issue": (
                        "Potential contradiction "
                        "or limitation detected"
                    )
                }
            )

    return contradictions



def detect_consensus(papers):

    consensus = []

    for paper in papers:

        abstract = (
            paper.get(
                "abstract",
                ""
            ).lower()
        )

        if (
            "significant" in abstract
            or "effective" in abstract
            or "strong evidence" in abstract
        ):

            consensus.append(
                {
                    "title": paper.get(
                        "title"
                    ),
                    "finding": (
                        "Positive evidence detected"
                    )
                }
            )

    return consensus



def detect_uncertainties(papers):

    uncertainties = []

    for paper in papers:

        abstract = (
            paper.get(
                "abstract",
                ""
            ).lower()
        )

        if (
            "more research" in abstract
            or "uncertain" in abstract
            or "unclear" in abstract
        ):

            uncertainties.append(
                {
                    "title": paper.get(
                        "title"
                    ),
                    "issue": (
                        "Research uncertainty detected"
                    )
                }
            )

    return uncertainties



def analyze_evidence_strength(papers):

    strong_sources = []

    weak_sources = []

    for paper in papers:

        credibility = paper.get(
            "credibility",
            0
        )

        if credibility >= 0.7:

            strong_sources.append(
                {
                    "title": paper.get(
                        "title"
                    ),
                    "credibility": credibility
                }
            )

        else:

            weak_sources.append(
                {
                    "title": paper.get(
                        "title"
                    ),
                    "credibility": credibility
                }
            )

    return {
        "strong_sources": strong_sources,
        "weak_sources": weak_sources
    }