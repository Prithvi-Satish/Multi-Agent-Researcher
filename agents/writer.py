from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.3)  # Use powerful model for quality

WRITER_PROMPT = """You are a research report writer. Write a comprehensive,
well-structured markdown report. Requirements:
- Start with an executive summary (2-3 sentences)
- Use ## headings for each major section
- Cite sources inline as [Source: URL]
- End with a ## Key Takeaways section (bullet points)
- Be factual, clear, and avoid padding"""

def writer_agent(state: dict) -> dict:
    context = "\n\n".join([
        f"### {r['question']}\n{r['answer']}"
        for r in state.get("search_results", [])
    ])
    
    response = llm.invoke([
        SystemMessage(content=WRITER_PROMPT),
        HumanMessage(content=f"Topic: {state['query']}\n\nResearch findings:\n{context}")
    ])
    return {"draft_report": response.content}
