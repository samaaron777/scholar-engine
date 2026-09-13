import streamlit as st
import json
import os

from datetime import datetime

from services.orchestrator import (
    orchestrate_research
)


# PAGE CONFIG

st.set_page_config(
    page_title="Scholar Engine",
    layout="wide"
)


# TITLE

st.title("Scholar Engine")

st.markdown(
    """
Advanced AI Research Infrastructure
"""
)


# USER INPUT

query = st.text_input(
    "Enter a research topic:"
)


# RUN RESEARCH

if st.button("Generate Report") and query:

    with st.spinner(
        "Running research pipeline..."
    ):

        try:

            results = orchestrate_research(
                query
            )

            
            
            # PAPERS
            

            st.header("Top Research Papers")

            papers = results.get(
                "papers",
                []
            )

            for paper in papers:

                st.subheader(
                    paper.get(
                        "title",
                        "Unknown Title"
                    )
                )

                st.write(
                    f"Authors: "
                    f"{paper.get('authors', 'Unknown')}"
                )

                st.write(
                    f"Year: "
                    f"{paper.get('year', 'Unknown')}"
                )

                st.write(
                    f"Citation Count: "
                    f"{paper.get('citationCount', 0)}"
                )

                st.write(
                    f"Credibility Score: "
                    f"{paper.get('credibility', 0)}"
                )

                st.write(
                    "Abstract:"
                )

                st.write(
                    paper.get(
                        "abstract",
                        "No abstract available."
                    )
                )

                st.write(
                    paper.get(
                        "url",
                        ""
                    )
                )

                st.divider()


            
            # REASONING ANALYSIS
            

            reasoning = results.get(
                "reasoning",
                {}
            )


            
            # CONSENSUS
            

            st.header(
                "Consensus Analysis"
            )

            consensus = reasoning.get(
                "consensus",
                []
            )

            if consensus:

                for item in consensus:

                    st.write(
                        f"• {item['title']}: "
                        f"{item['finding']}"
                    )

            else:

                st.write(
                    "No consensus patterns detected."
                )


            
            # CONTRADICTIONS
            

            st.header(
                "Contradictions"
            )

            contradictions = reasoning.get(
                "contradictions",
                []
            )

            if contradictions:

                for item in contradictions:

                    st.write(
                        f"• {item['title']}: "
                        f"{item['issue']}"
                    )

            else:

                st.write(
                    "No major contradictions detected."
                )


            
            # UNCERTAINTIES
            

            st.header(
                "Research Uncertainties"
            )

            uncertainties = reasoning.get(
                "uncertainties",
                []
            )

            if uncertainties:

                for item in uncertainties:

                    st.write(
                        f"• {item['title']}: "
                        f"{item['issue']}"
                    )

            else:

                st.write(
                    "No major uncertainties detected."
                )


            
            # EVIDENCE STRENGTH
            

            st.header(
                "Evidence Strength"
            )

            evidence_strength = reasoning.get(
                "evidence_strength",
                {}
            )

            strong_sources = evidence_strength.get(
                "strong_sources",
                []
            )

            weak_sources = evidence_strength.get(
                "weak_sources",
                []
            )


            # STRONG SOURCES

            st.subheader(
                "Strong Sources"
            )

            if strong_sources:

                for source in strong_sources:

                    st.write(
                        f"• {source['title']} "
                        f"(Score: "
                        f"{source['credibility']})"
                    )

            else:

                st.write(
                    "No strong sources detected."
                )


            # WEAK SOURCES

            st.subheader(
                "Weak Sources"
            )

            if weak_sources:

                for source in weak_sources:

                    st.write(
                        f"• {source['title']} "
                        f"(Score: "
                        f"{source['credibility']})"
                    )

            else:

                st.write(
                    "No weak sources detected."
                )


            
            # SAVE REPORT
        

            os.makedirs(
                "outputs",
                exist_ok=True
            )

            filename = (
                "outputs/report_"
                f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            )

            with open(
                filename,
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    results,
                    f,
                    indent=2
                )

            st.success(
                f"Saved report to {filename}"
            )


        except Exception as e:

            st.error(
                f"Error: {e}"
            )