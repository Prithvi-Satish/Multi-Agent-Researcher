import json
import re
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

CRITIC_PROMPT = """Review this research report and return JSON with:
{
  "passed": true/false,
  "issues": ["issue 1", "issue 2"],  // empty list if passed
  "improved_report": "full improved report text"  // only if not passed
}
Fail the report if: claims are unsupported, key aspects are missing,
or the structure is unclear. Pass if the report is factual and complete."""

def critic_agent(state: dict) -> dict:
    response = llm.invoke([
        SystemMessage(content=CRITIC_PROMPT),
        HumanMessage(content=f"Report to review:\n{state.get('draft_report', '')}")
    ])
    
    match = re.search(r'\{.*\}', response.content, re.DOTALL)
    result = json.loads(match.group()) if match else {"passed": True, "issues": []}
    
    if result.get("passed"):
        return {
            "critique_passed": True,
            "critique": "Report passed review.",
            "final_report": state["draft_report"]
        }
    else:
        issues = "\n".join(result.get("issues", []))
        improved = result.get("improved_report", state["draft_report"])
        return {
            "critique_passed": True,  # one revision max
            "critique": f"Issues found:\n{issues}",
            "final_report": improved
        }
