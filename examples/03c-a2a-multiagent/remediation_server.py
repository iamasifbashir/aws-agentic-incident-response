"""Remediation agent exposed as an A2A server on localhost:9000."""
import logging
from strands import Agent, tool
from strands.models import BedrockModel
from strands.multiagent.a2a import A2AServer
logging.basicConfig(level=logging.INFO)


@tool
def suggest_remediation(issue_description: str,
                        service_hint: str = "") -> str:
    """Propose a concrete remediation for an AWS issue.

    Args:
        issue_description: Plain-English description of what's wrong.
        service_hint: Optional AWS service name (e.g. "RDS", "EC2").
    """
    # In a real system this would consult a runbook index. For today
    # the deterministic reply keeps the example self-contained.
    return (
        f"For the reported issue ({issue_description!r}) on "
        f"service {service_hint or 'unspecified'}: "
        f"1) Check recent deployments in the last 24h. "
        f"2) Review CloudWatch alarm history for correlated events. "
        f"3) If transient, enable auto-scaling headroom. "
        f"Route to service team for permanent fix."
    )


def build_remediation_agent() -> Agent:
    model = BedrockModel(
        model_id="apac.amazon.nova-pro-v1:0",
        region_name="ap-southeast-2",
        temperature=0.3,
    )
    return Agent(
        name="Remediation Agent",
        description=("Proposes concrete remediations for AWS operational "
                     "issues. Call with a plain-language issue "
                     "description and an optional service hint."),
        model=model,
        tools=[suggest_remediation],
        system_prompt=(
            "You are a site reliability advisor. Given an issue, call "
            "suggest_remediation with a clean description and "
            "return the result directly to the caller."
        ),
    )


if __name__ == "__main__":
    agent = build_remediation_agent()
    server = A2AServer(
        agent=agent,
        host="0.0.0.0",
        port=9000,
        version="1.0.0",
    )
    logging.info("Remediation A2A server starting on http://localhost:9000")
    server.serve()
