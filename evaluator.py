from datetime import datetime
import math
import json

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv()


# ==========================================
# CONFIGURATION
# ==========================================

CURRENT_YEAR = datetime.now().year

MIN_QUALITY_FOR_UNDER_RECOGNIZED = 0.70

MAX_INFLUENCE_FOR_UNDER_RECOGNIZED = 0.35


# ==========================================
# LLM
# ==========================================

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0
)


# ==========================================
# CITATION INFLUENCE
# ==========================================

def normalize_citations(citation_count):

    if citation_count is None:
        return 0.0

    try:
        citation_count = max(
            0,
            int(citation_count)
        )

    except (ValueError, TypeError):
        return 0.0

    influence = (
        math.log10(citation_count + 1)
        / 5
    )

    return min(
        round(influence, 4),
        1.0
    )


# ==========================================
# RECENCY SCORE
# ==========================================

def calculate_recency_score(year):

    try:
        year = int(year)

    except (ValueError, TypeError):
        return 0.5

    age = CURRENT_YEAR - year

    if age <= 1:
        return 1.0

    if age <= 3:
        return 0.9

    if age <= 5:
        return 0.8

    if age <= 10:
        return 0.65

    if age <= 20:
        return 0.5

    return 0.4


# ==========================================
# CONTENT-BASED RESEARCH EVALUATION
# ==========================================

def evaluate_research_content(paper):

    title = paper.get(
        "title",
        "Unknown"
    )

    abstract = paper.get(
        "abstract",
        ""
    )

    authors = paper.get(
        "authors",
        ""
    )

    year = paper.get(
        "year",
        CURRENT_YEAR
    )


    # ==========================================
    # NO CONTENT AVAILABLE
    # ==========================================

    if not abstract:

        return {
            "methodological_rigor": 0.5,
            "evidence_strength": 0.5,
            "research_relevance": 0.5,
            "reproducibility": 0.5,
            "limitations_awareness": 0.5,
            "content_quality": 0.5,
            "reasoning": (
                "Insufficient research content was "
                "available for detailed evaluation."
            )
        }


    # ==========================================
    # EVALUATION PROMPT
    # ==========================================

    prompt = f"""
You are an expert research-methodology evaluator.

Evaluate the following research paper using ONLY
the information provided below.

Do not invent information that is not present.

------------------------------------------
PAPER
------------------------------------------

Title:
{title}

Authors:
{authors}

Publication Year:
{year}

Abstract:
{abstract}

------------------------------------------
EVALUATION PRINCIPLES
------------------------------------------

Evaluate the research independently of popularity.

IMPORTANT:

A high citation count does NOT prove that research
is methodologically strong.

A low citation count does NOT prove that research
is weak.

Citation count must NOT influence any of the
research-quality scores below.

Assess:

1. methodological_rigor

Consider:
- clarity of research methodology
- appropriateness of study design
- experimental design
- analytical rigor
- whether the methodology appears appropriate
  for the research question

2. evidence_strength

Consider:
- strength of evidence presented
- whether conclusions appear supported
- quality of reported findings
- strength of empirical or theoretical support

3. research_relevance

Consider:
- relevance to the research question
- significance of the research problem
- applicability of the findings

4. reproducibility

Consider:
- methodological transparency
- clarity of procedures
- whether another researcher could reasonably
  understand how the work was conducted

5. limitations_awareness

Consider:
- whether limitations are acknowledged
- whether conclusions appear appropriately cautious
- whether the authors distinguish evidence from
  speculation

6. content_quality

Provide an overall assessment of the research
content based on the above dimensions.

All scores must be between 0 and 1.

Do NOT infer quality from:
- citation count
- popularity
- search ranking
- number of authors
- fame of the authors

Return ONLY valid JSON.

Required format:

{{
    "methodological_rigor": 0.0,
    "evidence_strength": 0.0,
    "research_relevance": 0.0,
    "reproducibility": 0.0,
    "limitations_awareness": 0.0,
    "content_quality": 0.0,
    "reasoning": "brief explanation of the evaluation"
}}
"""


    # ==========================================
    # LLM EVALUATION
    # ==========================================

    try:

        response = llm.invoke(
            prompt
        )

        content = response.content

        if isinstance(
            content,
            list
        ):

            content = "".join(
                str(item)
                for item in content
            )

        content = content.strip()


        # ==========================================
        # CLEAN JSON
        # ==========================================

        content = content.replace(
            "```json",
            ""
        )

        content = content.replace(
            "```",
            ""
        )

        content = content.strip()


        # ==========================================
        # PARSE JSON
        # ==========================================

        evaluation = json.loads(
            content
        )


        # ==========================================
        # VALIDATE NUMERIC VALUES
        # ==========================================

        numeric_fields = [
            "methodological_rigor",
            "evidence_strength",
            "research_relevance",
            "reproducibility",
            "limitations_awareness",
            "content_quality"
        ]

        for field in numeric_fields:

            value = evaluation.get(
                field,
                0.5
            )

            try:

                value = float(
                    value
                )

            except (
                ValueError,
                TypeError
            ):

                value = 0.5

            evaluation[field] = max(
                0.0,
                min(
                    value,
                    1.0
                )
            )


        return evaluation


    except Exception as e:

        return {
            "methodological_rigor": 0.5,
            "evidence_strength": 0.5,
            "research_relevance": 0.5,
            "reproducibility": 0.5,
            "limitations_awareness": 0.5,
            "content_quality": 0.5,
            "reasoning": (
                f"Content evaluation failed: {e}"
            )
        }


# ==========================================
# CALCULATE CREDIBILITY
# ==========================================

def calculate_credibility(
    paper,
    content_evaluation=None
):

    # ------------------------------------------
    # If evaluation wasn't supplied, evaluate it.
    #
    # This preserves compatibility with existing
    # code that may call calculate_credibility(paper)
    # directly.
    # ------------------------------------------

    if content_evaluation is None:

        content_evaluation = (
            evaluate_research_content(
                paper
            )
        )


    # ==========================================
    # GET COMPONENTS
    # ==========================================

    content_quality = (
        content_evaluation.get(
            "content_quality",
            0.5
        )
    )

    methodological_rigor = (
        content_evaluation.get(
            "methodological_rigor",
            0.5
        )
    )

    evidence_strength = (
        content_evaluation.get(
            "evidence_strength",
            0.5
        )
    )

    research_relevance = (
        content_evaluation.get(
            "research_relevance",
            0.5
        )
    )

    year = paper.get(
        "year",
        CURRENT_YEAR
    )

    recency = calculate_recency_score(
        year
    )


    # ==========================================
    # RESEARCH QUALITY
    # ==========================================

    research_quality = (
        content_quality * 0.35
        +
        methodological_rigor * 0.25
        +
        evidence_strength * 0.20
        +
        research_relevance * 0.15
        +
        recency * 0.05
    )


    research_quality = max(
        0.0,
        min(
            research_quality,
            1.0
        )
    )


    return round(
        research_quality,
        4
    )


# ==========================================
# EVALUATE ONE PAPER
# ==========================================

def evaluate_paper(paper):

    # ==========================================
    # ONE LLM CALL
    # ==========================================

    content_evaluation = (
        evaluate_research_content(
            paper
        )
    )


    # ==========================================
    # CALCULATE QUALITY
    # ==========================================

    credibility = calculate_credibility(
        paper,
        content_evaluation
    )


    # ==========================================
    # CITATION INFLUENCE
    # ==========================================

    citation_influence = (
        normalize_citations(
            paper.get(
                "citationCount",
                0
            )
        )
    )


    # ==========================================
    # ATTACH EVALUATION
    # ==========================================

    paper["credibility"] = (
        credibility
    )

    paper["citation_influence"] = (
        citation_influence
    )

    paper["methodological_rigor"] = (
        content_evaluation.get(
            "methodological_rigor",
            0.5
        )
    )

    paper["evidence_strength"] = (
        content_evaluation.get(
            "evidence_strength",
            0.5
        )
    )

    paper["research_relevance"] = (
        content_evaluation.get(
            "research_relevance",
            0.5
        )
    )

    paper["reproducibility"] = (
        content_evaluation.get(
            "reproducibility",
            0.5
        )
    )

    paper["limitations_awareness"] = (
        content_evaluation.get(
            "limitations_awareness",
            0.5
        )
    )

    paper["content_quality"] = (
        content_evaluation.get(
            "content_quality",
            0.5
        )
    )

    paper["evaluation_reasoning"] = (
        content_evaluation.get(
            "reasoning",
            ""
        )
    )


    # ==========================================
    # UNDER-RECOGNIZED ANALYSIS
    # ==========================================

    under_recognized = (
        detect_under_recognized(
            paper
        )
    )


    paper["under_recognized"] = (
        under_recognized[
            "under_recognized"
        ]
    )

    paper["under_recognized_score"] = (
        under_recognized[
            "under_recognized_score"
        ]
    )

    paper["under_recognized_reasoning"] = (
        under_recognized[
            "reasoning"
        ]
    )


    return paper


# ==========================================
# EVALUATE MULTIPLE PAPERS
# ==========================================

def evaluate_papers(papers):

    evaluated = []

    for paper in papers:

        evaluated.append(
            evaluate_paper(
                paper
            )
        )

    return evaluated


# ==========================================
# UNDER-RECOGNIZED SCORE
# ==========================================

def calculate_under_recognized_score(
    paper
):

    quality = paper.get(
        "credibility",
        0
    )

    citation_influence = paper.get(
        "citation_influence",
        normalize_citations(
            paper.get(
                "citationCount",
                0
            )
        )
    )


    recognition_gap = (
        1.0 - citation_influence
    )


    # Quality remains dominant.
    #
    # Citation influence is only used to identify
    # relatively under-recognized research.

    score = (
        quality * 0.75
        +
        recognition_gap * 0.25
    )


    return round(
        score,
        4
    )


# ==========================================
# UNDER-RECOGNIZED DETECTOR
# ==========================================

def detect_under_recognized(
    paper
):

    quality = paper.get(
        "credibility",
        0
    )

    citation_influence = paper.get(
        "citation_influence",
        0
    )

    score = (
        calculate_under_recognized_score(
            paper
        )
    )


    # ==========================================
    # QUALITY THRESHOLD
    # ==========================================

    if quality < (
        MIN_QUALITY_FOR_UNDER_RECOGNIZED
    ):

        return {
            "under_recognized": False,
            "under_recognized_score": score,
            "reasoning": (
                "Research quality did not meet "
                "the threshold required for "
                "under-recognized classification."
            )
        }


    # ==========================================
    # INFLUENCE THRESHOLD
    # ==========================================

    if citation_influence > (
        MAX_INFLUENCE_FOR_UNDER_RECOGNIZED
    ):

        return {
            "under_recognized": False,
            "under_recognized_score": score,
            "reasoning": (
                "The paper already has substantial "
                "scholarly influence relative to "
                "the current threshold."
            )
        }


    # ==========================================
    # FLAG AS CANDIDATE
    # ==========================================

    return {
        "under_recognized": True,
        "under_recognized_score": score,
        "reasoning": (
            "The paper demonstrates relatively "
            "strong research-quality characteristics "
            "while receiving comparatively limited "
            "scholarly attention. It may warrant "
            "additional human inspection."
        )
    }


# ==========================================
# STANDARD RESEARCH RANKING
# ==========================================

def rank_papers(papers):

    return sorted(
        papers,
        key=lambda paper: (
            paper.get(
                "credibility",
                0
            )
        ),
        reverse=True
    )


# ==========================================
# UNDER-RECOGNIZED RESEARCH RANKING
# ==========================================

def rank_under_recognized(
    papers
):

    candidates = [
        paper
        for paper in papers
        if paper.get(
            "under_recognized",
            False
        )
    ]


    return sorted(
        candidates,
        key=lambda paper: (
            paper.get(
                "under_recognized_score",
                0
            )
        ),
        reverse=True
    )