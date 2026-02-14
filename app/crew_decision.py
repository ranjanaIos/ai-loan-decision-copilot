from crewai import Agent, Task, Crew
from crewai.tools import tool
from app.rag import ask_question
from crewai import LLM
from pydantic import BaseModel
import json
from app.policy_engine import enforce_policy


@tool("Company Policy Reader")
def policy_tool(question: str) -> str:
    """Reads company policy documents and returns relevant rules"""
    return ask_question(question) 

class LoanDecision(BaseModel):
    decision: str
    reason: str
    violated_rules: list[str]

ollama_llm = LLM(
    model="ollama/llama3:8b",
    base_url="http://localhost:11434"
)

researcher = Agent(
    role="Policy Research Analyst",
    goal="Find relevant company policy rules",
    backstory="Expert at reading company documents and extracting rules.",
    verbose=True,
    allow_delegation=False,
    tools=[policy_tool],
    llm=ollama_llm
)

risk_officer = Agent(
    role="Risk Officer",
    goal="Evaluate financial risk",
    backstory="Bank risk officer who identifies risky applications.",
    verbose=True,
    llm=ollama_llm
)

compliance_officer = Agent(
    role="Compliance Officer",
    goal="Ensure company policy compliance",
    backstory="Ensures rules are followed strictly.",
    verbose=True,
    llm=ollama_llm
)

manager = Agent(
    role="Loan Approval Manager",
    goal="Make final decision in strict JSON format",
    backstory="Responsible for approving or rejecting loans based on policy and must return structured JSON output.",
    verbose=True,
    llm=ollama_llm
)

def run_crew_decision(data: dict):

    research_task = Task(
        description=f"""
Read company policy related to:
Loan amount: {data['loan_amount']}
Credit score: {data['credit_score']}
DTI: {data['dti']}
""",
        expected_output="Relevant company policy rules related to this loan application.",
        agent=researcher
    )

    risk_task = Task(
        description=f"""
Evaluate financial risk for:
Credit score: {data['credit_score']}
Debt-to-income ratio: {data['dti']}
""",
        expected_output="Risk assessment: LOW, MEDIUM, or HIGH with reasoning.",
        agent=risk_officer
    )

    compliance_task = Task(
        description="Check if the loan violates any company policy rules.",
        expected_output="List of violated rules or confirmation of compliance.",
        agent=compliance_officer
    )

    decision_task = Task(
    description=f"""
Based on previous analysis, return FINAL DECISION.

You MUST return valid JSON only.
No explanations outside JSON.

Format:
{{
  "decision": "APPROVE or REJECT",
  "reason": "short explanation",
  "violated_rules": ["rule1","rule2"]
}}
""",
    agent=manager,
    expected_output="Valid JSON decision"
)

    crew = Crew(
        agents=[researcher, risk_officer, compliance_officer, manager],
        tasks=[research_task, risk_task, compliance_task, decision_task],
        verbose=True
    )

    result = crew.kickoff()

    try:
        parsed = json.loads(str(result))
        ai_decision = LoanDecision(**parsed).model_dump()
    except Exception:
        ai_decision = {"decision": "UNKNOWN", "reason": str(result), "violated_rules": []}

    # HARD GUARDRAIL (real-world pattern)
    rule_decision = enforce_policy(data)

    final = {
        "decision": rule_decision["decision"],
        "violated_rules": rule_decision["violated_rules"],
        "ai_reasoning": ai_decision.get("reason", "")
    }

    return final