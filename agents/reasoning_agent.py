from reasoning import (
    detect_contradictions,
    detect_consensus,
    detect_uncertainties,
    analyze_evidence_strength
)


def reasoning_agent(papers):

    contradictions = (
        detect_contradictions(papers)
    )

    consensus = (
        detect_consensus(papers)
    )

    uncertainties = (
        detect_uncertainties(papers)
    )

    evidence_strength = (
        analyze_evidence_strength(papers)
    )

    return {
        "contradictions": contradictions,
        "consensus": consensus,
        "uncertainties": uncertainties,
        "evidence_strength": evidence_strength
    }