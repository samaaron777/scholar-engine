def detect_contradictions(papers):

    contradictions = []

    for i in range(len(papers)):
        for j in range(i + 1, len(papers)):

            paper_a = papers[i]
            paper_b = papers[j]

            if (
                "increase" in paper_a["abstract"].lower()
                and
                "no effect" in paper_b["abstract"].lower()
            ):

                contradictions.append(
                    f"{paper_a['title']} contradicts {paper_b['title']}"
                )

    return contradictions