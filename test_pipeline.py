from services.orchestrator import orchestrate_research


def main():

    query = (
        "What are current approaches to "
        "detecting hallucinations in large language models?"
    )

    print("\n" + "=" * 70)
    print("SCHOLAR ENGINE TEST")
    print("=" * 70)

    print("\nQuery:")
    print(query)

    print("\nRunning research pipeline...")
    print("This may take a little while.\n")

    try:

        result = orchestrate_research(
            query
        )

        print("\n" + "=" * 70)
        print("PIPELINE COMPLETED")
        print("=" * 70)

        # ----------------------------------------------------
        # PAPERS
        # ----------------------------------------------------

        papers = result.get(
            "papers",
            []
        )

        print(
            f"\nPapers evaluated: {len(papers)}"
        )

        for index, paper in enumerate(
            papers[:5],
            start=1
        ):

            print("\n" + "-" * 60)

            print(
                f"{index}. "
                f"{paper.get('title')}"
            )

            print(
                f"Year: "
                f"{paper.get('year')}"
            )

            print(
                f"Citations: "
                f"{paper.get('citationCount')}"
            )

            print(
                f"Credibility: "
                f"{paper.get('credibility')}"
            )

            print(
                f"Under-recognized: "
                f"{paper.get('under_recognized')}"
            )

        # ----------------------------------------------------
        # UNDER-RECOGNIZED
        # ----------------------------------------------------

        under_recognized = result.get(
            "under_recognized",
            []
        )

        print("\n" + "=" * 70)
        print("UNDER-RECOGNIZED RESEARCH")
        print("=" * 70)

        print(
            f"\nCandidates: "
            f"{len(under_recognized)}"
        )

        for index, paper in enumerate(
            under_recognized[:5],
            start=1
        ):

            print("\n" + "-" * 60)

            print(
                f"{index}. "
                f"{paper.get('title')}"
            )

            print(
                f"Credibility: "
                f"{paper.get('credibility')}"
            )

            print(
                f"Citation influence: "
                f"{paper.get('citation_influence')}"
            )

            print(
                f"Under-recognized score: "
                f"{paper.get('under_recognized_score')}"
            )

        # ----------------------------------------------------
        # REASONING
        # ----------------------------------------------------

        reasoning = result.get(
            "reasoning",
            {}
        )

        print("\n" + "=" * 70)
        print("REASONING")
        print("=" * 70)

        print(
            reasoning
        )

        print("\n" + "=" * 70)
        print("TEST FINISHED")
        print("=" * 70)

    except Exception as e:

        print("\n" + "=" * 70)
        print("PIPELINE ERROR")
        print("=" * 70)

        print(
            f"\n{type(e).__name__}: {e}"
        )


if __name__ == "__main__":
    main()