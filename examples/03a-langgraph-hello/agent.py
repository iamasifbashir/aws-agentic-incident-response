"""LangGraph ReAct agent using Bedrock Nova Pro (APAC CRIS)."""

from langchain_aws import ChatBedrockConverse
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent


@tool
def get_cloudwatch_alarm_state(alarm_name: str) -> str:
    """Return the current state of a named CloudWatch alarm.

    Use this tool when the user asks about a specific alarm by name.

    Args:
        alarm_name: The exact CloudWatch alarm name.
    """
    # Stub implementation for the hello-world; real boto3 call would
    # go here. Returning a deterministic response keeps this example
    # self-contained for quick learning.
    return f"Alarm '{alarm_name}' is in state OK."


@tool
def list_alarms_in_alarm_state() -> str:
    """List all CloudWatch alarms currently in ALARM state.

    Use this tool when the user asks what's on fire right now.
    """
    return "No alarms are currently in ALARM state."


def build_agent():
    model = ChatBedrockConverse(
        model="apac.amazon.nova-pro-v1:0",
        region_name="ap-southeast-2",
        temperature=0.3,
    )
    return create_react_agent(
        model=model,
        tools=[get_cloudwatch_alarm_state, list_alarms_in_alarm_state],
        prompt=(
            "You are an on-call SRE assistant. Use tools to check "
            "alarm state when the user asks. Be concise."
        ),
    )


if __name__ == "__main__":
    agent = build_agent()
    response = agent.invoke({
        "messages": [
            {"role": "user",
             "content": "Is everything healthy right now?"}
        ]
    })
    for msg in response["messages"]:
        print(f"[{msg.type}] {msg.content}")
