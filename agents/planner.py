import json
import re
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

PLANNER_PROMPT = """You are a research planner. Given a research topic,
break it into exactly 3 focused sub-questions that together cover the topic
comprehensively. Return ONLY a JSON array of strings, nothing else.

Example output: ["What is X?", "How does X work?", "What is the future of X?"]"""

def planner_agent(state: dict) -> dict:
    response = llm.invoke([
        SystemMessage(content=PLANNER_PROMPT),
        HumanMessage(content=f"Research topic: {state['query']}")
    ])
    # Parse JSON from response
    match = re.search(r'\[.*\]', response.content, re.DOTALL)
    sub_questions = json.loads(match.group()) if match else [state['query']]
    return {"sub_questions": sub_questions}
