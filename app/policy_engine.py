def enforce_policy(data: dict):
    violations = []

    if data["credit_score"] < 650:
        violations.append("credit_score_below_650")

    if data["loan_amount"] > 500000:
        violations.append("collateral_required")

    if data["dti"] > 45:
        violations.append("high_dti_manual_review")

    if violations:
        return {
            "decision": "REJECT",
            "violated_rules": violations
        }

    return {"decision": "APPROVE", "violated_rules": []}