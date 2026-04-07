from tools.search_tool import tavily_search
from tools.scrape_tool import scrape_page
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

def searcher_agent(state: dict) -> dict:
    all_results = []
    all_sources = []

    for question in state.get("sub_questions", []):
        # Search for top 2 results per sub-question to save tokens
        results = tavily_search(question, max_results=2)
        
        # Scrape full content from each result
        context_chunks = []
        for r in results:
            content = scrape_page(r["url"])
            context_chunks.append(f"Source: {r['url']}\n{content}")
            all_sources.append(r["url"])
        
        # Summarize findings for this sub-question
        combined = "\n\n---\n\n".join(context_chunks)
        summary = llm.invoke([
            SystemMessage(content="Summarize the key facts from these sources that answer the question. Be concise and cite sources by URL."),
            HumanMessage(content=f"Question: {question}\n\nSources:\n{combined}")
        ])
        
        all_results.append({
            "question": question,
            "answer": summary.content,
            "sources": [r["url"] for r in results]
        })

    return {"search_results": all_results, "sources": list(set(all_sources))}
