from agents.retrieval_agent import retrieval_agent
from agents.evaluator_agent import evaluator_agent
from agents.reasoning_agent import reasoning_agent



# EXTRACT PAPERS


def extract_papers(results):

    papers = []

    semantic_data = results.get(
        "semantic_scholar",
        ""
    )

    if not semantic_data:
        return papers

    sections = semantic_data.split(
        "Title:"
    )

    for section in sections:

        if not section.strip():
            continue

        paper = {
            "title": "",
            "authors": "",
            "year": 2000,
            "citationCount": 0,
            "abstract": "",
            "url": ""
        }

        lines = section.splitlines()

        
        # TITLE
        

        if lines:

            paper["title"] = (
                lines[0]
                .strip()
            )

        
        # PARSE METADATA
        

        current_field = None

        for line in lines[1:]:

            line = line.strip()

            if not line:
                continue

            
            # AUTHORS
            

            if line.startswith("Authors:"):

                paper["authors"] = (
                    line
                    .replace(
                        "Authors:",
                        "",
                        1
                    )
                    .strip()
                )

                current_field = "authors"

            
            # YEAR
            

            elif line.startswith("Year:"):

                try:

                    paper["year"] = int(
                        line
                        .replace(
                            "Year:",
                            "",
                            1
                        )
                        .strip()
                    )

                except ValueError:

                    paper["year"] = 2000

                current_field = "year"

            
            # CITATION COUNT
            

            elif line.startswith(
                "Citation Count:"
            ):

                current_field = (
                    "citationCount"
                )

                value = (
                    line
                    .replace(
                        "Citation Count:",
                        "",
                        1
                    )
                    .strip()
                )

                if value:

                    try:

                        paper[
                            "citationCount"
                        ] = int(value)

                    except ValueError:

                        paper[
                            "citationCount"
                        ] = 0

            
            # ABSTRACT
            

            elif line.startswith(
                "Abstract:"
            ):

                paper["abstract"] = (
                    line
                    .replace(
                        "Abstract:",
                        "",
                        1
                    )
                    .strip()
                )

                current_field = "abstract"

            
            # URL
            

            elif line.startswith("URL:"):

                paper["url"] = (
                    line
                    .replace(
                        "URL:",
                        "",
                        1
                    )
                    .strip()
                )

                current_field = "url"

            
            # CONTINUATION OF ABSTRACT
            

            elif current_field == "abstract":

                paper["abstract"] += (
                    " " + line
                )

            
            # CONTINUATION OF AUTHORS
            

            elif current_field == "authors":

                paper["authors"] += (
                    " " + line
                )

            
            # IGNORE OTHER LINES
            

            else:

                continue

        
        # VALIDATE PAPER
        

        if paper["title"]:

            papers.append(
                paper
            )

    return papers



# RESEARCH ORCHESTRATOR


def orchestrate_research(
    query: str
):

    
    # 1. RETRIEVAL
    

    retrieval_results = (
        retrieval_agent(
            query
        )
    )

    
    # 2. EXTRACT STRUCTURED PAPERS
    

    papers = extract_papers(
        retrieval_results
    )

    
    # 3. EVALUATION + RANKING
    

    evaluation_results = (
        evaluator_agent(
            papers
        )
    )

    ranked_papers = (
        evaluation_results[
            "ranked_papers"
        ]
    )

    under_recognized = (
        evaluation_results[
            "under_recognized"
        ]
    )

    
    # 4. REASONING
    

    reasoning_results = (
        reasoning_agent(
            ranked_papers
        )
    )

    
    # 5. RETURN RESEARCH STATE
    

    return {

        "query": query,

        "papers": ranked_papers,

        "under_recognized": (
            under_recognized
        ),

        "reasoning": (
            reasoning_results
        ),

        "raw_results": (
            retrieval_results
        )
    }