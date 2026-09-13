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



# QUERY DECOMPOSITION AGENT


def decomposition_agent(query):

    prompt = f"""
You are an advanced AI research planner.

Your task:
Break the research question into smaller,
high-quality research sub-questions.

Research Question:
{query}

Rules:
- Create focused sub-questions
- Avoid duplicates
- Cover different dimensions
- Think like a professional researcher
- Generate between 3 and 7 sub-questions

Return ONLY the sub-questions.
"""

    response = llm.invoke(prompt)

    lines = response.content.split("\n")

    sub_queries = []

    for line in lines:

        cleaned = line.strip()

        if cleaned:

            cleaned = (
                cleaned
                .replace("-", "")
                .replace("*", "")
                .strip()
            )

            sub_queries.append(cleaned)

    return sub_queries