"""Monitoring agent that delegates to the remediation A2A server."""
from strands import Agent, tool
from strands.models import BedrockModel
from strands_tools.a2a_client import A2AClientToolProvider


@tool
def simulate_cloudwatch_check() -> str:
    """Simulate checking CloudWatch for operational anomalies.

    In a real system this would call boto3. For this learning example
    we return a deterministic 'something is wrong' response so the
    agent has a reason to delegate to the remediation agent.
    """
    return (
        "ANOMALY DETECTED: RDS instance 'prod-orders-db' CPU has been "
        "above 90% for the last 30 minutes. No recent deployments. "
        "No correlated application errors."
    )


def build_monitoring_agent() -> Agent:
    # The A2A client tool provider discovers the remediation agent
    # via its Agent Card and exposes it as a callable tool.
    a2a_tools = A2AClientToolProvider(
        known_agent_urls=["http://localhost:9000"]
    )
    
    model = BedrockModel(
        model_id="apac.amazon.nova-pro-v1:0",
        region_name="ap-southeast-2",
        temperature=0.3,
    )
    return Agent(
        name="Monitoring Agent",
        model=model,
        tools=[simulate_cloudwatch_check, *a2a_tools.tools],
        system_prompt=(
            "You are a monitoring agent. When checking for anomalies, "
            "use simulate_cloudwatch_check first. If you find an "
            "anomaly, delegate the remediation analysis to the "
            "Remediation Agent via A2A. Return both the finding and "
            "the remediation recommendation to the user."
        ),
    )


if __name__ == "__main__":
    agent = build_monitoring_agent()
    result = agent(
        "Check for any operational issues and get a remediation plan "
        "for anything you find."
    )
    print("\n" + "=" * 60)
    print("FINAL ANSWER")
    print("=" * 60)
    print(result)
