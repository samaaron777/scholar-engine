from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List

from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from langchain.agents import (
    create_tool_calling_agent,
    AgentExecutor
)

from tools import (
    search_tool,
    wiki_tool,
    save_tool,
    arxiv,
    semantic_scholar_tool,
    memory_search_tool
)

load_dotenv()


# ==========================================
# PYDANTIC MODELS
# ==========================================

class Source(BaseModel):
    title: str
    authors: List[str]
    year: int
    citation_count: int
    abstract: str
    url: str
    source_type: str
    credibility: float
    reasoning: str


class ResearchResponse(BaseModel):
    topic: str
    summary: str
    key_points: List[str]
    contradictions: List[str]
    recommended_readings: List[str]
    sources: List[Source]
    tools_used: List[str]


# ==========================================
# LLM
# ==========================================

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0
)


# ==========================================
# OUTPUT PARSER
# ==========================================

parser = PydanticOutputParser(
    pydantic_object=ResearchResponse
)


# ==========================================
# PROMPT
# ==========================================

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an advanced AI research copilot.

Your job is NOT merely to search for information.

You must:
- retrieve evidence
- evaluate evidence quality
- compare sources
- rank credibility
- identify contradictions
- synthesize findings
- explain reasoning

Research Rules:
- Prefer Semantic Scholar and arXiv for academic research
- Use Wikipedia and web search mainly for supplemental information
- Prioritize:
    - highly cited papers
    - peer-reviewed sources
    - authoritative institutions
    - recent research
    - strong evidence

Avoid:
- weak evidence
- low credibility sources
- unverified claims
- SEO-driven content

For every source:
- explain WHY it is credible
- include credibility score from 0 to 1

You are a RESEARCH ENGINE, not a chatbot.

Your response MUST follow this exact schema:

{format_instructions}
"""
        ),

        ("placeholder", "{chat_history}"),

        (
            "human",
            "{query}"
        ),

        ("placeholder", "{agent_scratchpad}")
    ]
).partial(
    format_instructions=parser.get_format_instructions()
)


# ==========================================
# TOOLS
# ==========================================

tools = [
    search_tool,
    wiki_tool,
    save_tool,
    arxiv,
    semantic_scholar_tool,
    memory_search_tool
]


# ==========================================
# AGENT
# ==========================================

agent = create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=tools
)


# ==========================================
# EXECUTOR
# ==========================================

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True
)