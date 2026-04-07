import streamlit as st
import os
from dotenv import load_dotenv
load_dotenv()
from graph import research_graph
from state import ResearchState

st.set_page_config(page_title="Research Assistant", layout="wide")
st.title("Multi-agent research assistant")
st.caption("Powered by LangGraph + GPT-4o + Tavily")

query = st.text_input(
    "Enter your research topic",
    placeholder="e.g. What is the future of nuclear energy?"
)

if st.button("Research", type="primary") and query:
    initial_state: ResearchState = {
        "query": query, 
        "sub_questions": [], 
        "search_results": [],
        "draft_report": None, 
        "critique": None,
        "critique_passed": False, 
        "final_report": None, 
        "sources": []
    }

    # Live progress display
    with st.status("Running research agents...", expanded=True) as status:
        for step in research_graph.stream(initial_state):
            for step_name, step_state in step.items():
                if "planner" in step_name:
                    st.write("Planner: breaking query into sub-questions")
                    for q in step_state.get("sub_questions", []):
                        st.caption(f"  — {q}")
                
                elif "searcher" in step_name:
                    st.write("Searcher: gathering sources from the web")
                    n = len(step_state.get("search_results", []))
                    st.caption(f"  — Found results for {n} sub-questions")
                
                elif "writer" in step_name:
                    st.write("Writer: drafting the report")
                
                elif "critic" in step_name:
                    st.write("Critic: reviewing report quality")
                    st.caption(f"  — {step_state.get('critique', '')}")
        
        status.update(label="Research complete!", state="complete")

    # Final outputs
    final = research_graph.invoke(initial_state)

    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("## Report")
        st.markdown(final.get("final_report", "No report generated."))
    
    with col2:
        st.markdown("## Sources")
        for url in final.get("sources", [])[:10]:
            st.markdown(f"- [{url[:50]}...]({url})")
