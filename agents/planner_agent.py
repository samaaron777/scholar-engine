from dotenv import load_dotenv

from langchain_google_genai import (
    ChatGoogleGenerativeAI
)

load_dotenv()


# ==========================================
# LLM
# ==========================================

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0
)


# ==========================================
# PLANNING AGENT
# ==========================================

def planner_agent(query):

    prompt = f"""
You are an advanced AI research planner.

Your task:
- Analyze the user's research question
- Break it into smaller research tasks
- Identify what evidence is needed
- Create a structured research plan

Research Question:
{query}

Generate:

1. Core Research Question
2. Important Subtopics
3. Required Evidence Types
4. Key Research Areas
5. Potential Contradictions
6. Important Context
7. Recommended Retrieval Strategy

Be analytical and structured.
"""

    response = llm.invoke(prompt)

    return response.content