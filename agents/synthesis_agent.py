from dotenv import load_dotenv

from langchain_google_genai import (
    ChatGoogleGenerativeAI
)

load_dotenv()



# LLM


llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0
)



# SYNTHESIS AGENT


def synthesis_agent(
    query,
    ranked_papers,
    reasoning_output
):

    
    
    # FORMAT PAPERS
    

    papers_text = ""

    for paper in ranked_papers:

        papers_text += f"""
Title: {paper.get('title', 'Unknown')}

Authors: {paper.get('authors', 'Unknown')}

Year: {paper.get('year', 'Unknown')}

Citation Count: {paper.get('citationCount', 0)}

Credibility Score: {paper.get('credibility', 0)}

Abstract:
{paper.get('abstract', 'No abstract available')}

URL:
{paper.get('url', 'No URL')}

----------------------------------------
"""


    
    
    # FORMAT REASONING OUTPUT
    

    contradictions = reasoning_output.get(
        "contradictions",
        []
    )

    consensus = reasoning_output.get(
        "consensus",
        []
    )

    uncertainties = reasoning_output.get(
        "uncertainties",
        []
    )

    evidence_strength = reasoning_output.get(
        "evidence_strength",
        {}
    )


    reasoning_text = f"""
Consensus Findings:
{consensus}

Contradictions:
{contradictions}

Uncertainties:
{uncertainties}

Evidence Strength:
{evidence_strength}
"""


    
    
    # PROMPT
    

    prompt = f"""
You are an advanced AI research analyst.

Your responsibilities:
- Analyze research evidence carefully
- Prioritize high-credibility papers
- Identify important findings
- Explain contradictions
- Explain uncertainty
- Produce professional research synthesis

Research Topic:
{query}

Research Papers:
{papers_text}

Reasoning Analysis:
{reasoning_text}

Generate the following sections:

1. Executive Summary

2. Key Findings

3. Evidence Quality Assessment

4. Consensus Analysis

5. Contradictions and Limitations

6. Research Uncertainties

7. Final Research Conclusion

Be analytical, objective, and evidence-focused.
"""


    
    
    # LLM RESPONSE
    

    response = llm.invoke(prompt)

    
    
    # RETURN FINAL SYNTHESIS
    

    return response.content