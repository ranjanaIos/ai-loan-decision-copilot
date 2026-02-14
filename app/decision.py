from app.rag import ask_question


def evaluate_loan(data: dict):
    context_question = f"""
Company policy context:

Loan amount: {data['loan_amount']}
Credit score: {data['credit_score']}
Debt-to-income ratio: {data['dti']}

Based on company policy, should this loan be approved or rejected?
Explain the reason and reference policy rules.
Return final answer as:
DECISION: APPROVE or REJECT
REASON: <short explanation>
"""

    response = ask_question(context_question)

    decision = "REJECT"
    if "APPROVE" in response.upper():
        decision = "APPROVE"

    return {
        "decision": decision,
        "analysis": response
    }