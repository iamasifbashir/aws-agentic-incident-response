"""AWS Cost Investigator Agent (Strands + Nova Pro)."""
from strands import Agent
from strands.models import BedrockModel
from .tools.cost_tools import get_cost_by_service
from .tools.cloudwatch_tools import get_cloudwatch_alarm_state
from .tools.remediation_tools import draft_remediation_note

SYSTEM_PROMPT = """You are a FinOps analyst for AWS workloads. Your job
is to investigate cost anomalies and draft clear, actionable
recommendations for the engineering team.

HOW TO APPROACH A COST QUESTION:
1. Start with get_cost_by_service to see which services are driving
 spend. Look at the percentage change vs the previous window.
2. For services with unusual spikes, call get_cloudwatch_alarm_state
 with that service name as the filter. Correlate cost spikes with
 alarm events.
3. Once you have a clear finding, use draft_remediation_note to
 produce a formatted summary. Pick severity based on magnitude:
 low (<20% change), medium (20-100%), high (>100%), critical
 (any production alarm firing alongside a cost spike).

OUTPUT:
End with the remediation note. Before it, briefly summarise what you
checked and what you found, in your own words.

CONSTRAINTS:
- Never recommend deleting or modifying resources directly. Only
 suggest human review.
- If the evidence is thin or ambiguous, say so clearly rather than
 guessing.
- Keep your reasoning concise. The reader is an engineer who wants
 the answer, not a lecture.
"""


def build_agent() -> Agent:
    model = BedrockModel(
        model_id="apac.amazon.nova-pro-v1:0",
        region_name="ap-southeast-2",
        temperature=0.3,
        streaming=True,
    )
    return Agent(
        model=model,
        tools=[
            get_cost_by_service,
            get_cloudwatch_alarm_state,
            draft_remediation_note,
        ],
        system_prompt=SYSTEM_PROMPT,
    )


if __name__ == "__main__":
    agent = build_agent()
    question = (
        "Our AWS bill in February this year looks higher than usual. Can you "
        "investigate what's going on and draft a note for the team?"
    )
    print(f"USER: {question}\n")
    result = agent(question)
    print("\n" + "=" * 60)
    print("FINAL ANSWER")
    print("=" * 60)
    print(result)
