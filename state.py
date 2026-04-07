from typing import TypedDict, List, Optional

class ResearchState(TypedDict):
    # Input
    query: str

    # Planner output
    sub_questions: List[str]

    # Searcher output (one entry per sub-question)
    search_results: List[dict]   # [{question, content, sources}]

    # Writer output
    draft_report: Optional[str]

    # Critic output
    critique: Optional[str]
    critique_passed: bool

    # Final output
    final_report: Optional[str]
    sources: List[str]
