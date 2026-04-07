import os
from dotenv import load_dotenv
load_dotenv()
from graph import research_graph
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
import json
import re

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

TEST_QUERIES = [
    "What is quantum computing?",
    "How does CRISPR gene editing work?",
    "What are the risks of AI in healthcare?"
]

def score_report(query: str, report: str) -> dict:
    if not report:
        return {"error": "Report is empty"}
        
    prompt = f"""Score this research report on the topic '{query}' from 1-5 on:
- Completeness: Does it cover all key aspects?
- Accuracy: Are claims well-supported?
- Clarity: Is it well-structured and readable?

Return JSON: {{"completeness": N, "accuracy": N, "clarity": N, "overall": N}}

Report:
{report[:2000]}"""
    
    resp = llm.invoke([HumanMessage(content=prompt)])
    return extract_json(resp.content)

def extract_json(text):
    m = re.search(r'\{.*\}', text, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(), strict=False)
        except json.JSONDecodeError:
            return {}
    return {}

if __name__ == "__main__":
    for query in TEST_QUERIES:
        state = {"query": query, "sub_questions": [], "search_results": [],
                 "draft_report": None, "critique": None,
                 "critique_passed": False, "final_report": None, "sources": []}
        print(f"\nEvaluating query: {query}")
        result = research_graph.invoke(state)
        scores = score_report(query, result.get("final_report"))
        print(f"Scores: {scores}")
