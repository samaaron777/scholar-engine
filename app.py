import streamlit as st
from main import agent_executor, parser
import os
from datetime import datetime

st.set_page_config(
    page_title="AI Research Copilot",
    layout="wide"
)

st.title("AI Research Copilot")
st.write("Generate structured, source-backed research summaries.")

query = st.text_input(
    "Enter a research topic:"
)

if st.button("Generate Report") and query:

    with st.spinner("Researching..."):

        try:

            raw_response = agent_executor.invoke(
                {"query": query}
            )

            output = raw_response.get("output")

            print("\nRAW OUTPUT:\n")
            print(output)

            structured = parser.parse(output)

            
            # Display Topic
            

            st.subheader("📌 Topic")
            st.write(structured.topic)

            
            # Display Summary
            

            st.subheader("📝 Summary")
            st.write(structured.summary)

            
            # Display Key Points
            

            st.subheader("🔑 Key Points")

            for point in structured.key_points:
                st.write(f"- {point}")

            
            # Display Sources
            

            st.subheader("📚 Sources")

            for s in structured.sources:

                st.markdown(f"### {s.title}")

                st.write(f"Type: {s.source_type}")
                st.write(f"Credibility: {s.credibility}")
                st.write(s.url)

            
            # Display Tools Used
            

            st.subheader("🛠 Tools Used")

            for tool in structured.tools_used:
                st.write(f"- {tool}")

            
            # Save Output
            

            os.makedirs("outputs", exist_ok=True)

            filename = (
                f"outputs/report_"
                f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            )

            with open(filename, "w") as f:
                f.write(
                    structured.model_dump_json(indent=2)
                )

            st.success(f"Saved report to {filename}")

        except Exception as e:

            st.error(f"Error: {e}")