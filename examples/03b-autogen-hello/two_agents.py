"""AutoGen two-agent conversation (learning example).
Demonstrates the assistant + user-proxy pattern, with Bedrock Nova Pro
as the LLM backend. The goal is to see the multi-agent conversation
pattern, not to build anything useful.
"""
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_ext.models.openai import OpenAIChatCompletionClient


def build_bedrock_client():
    # LiteLLM exposes Bedrock models through an OpenAI-compatible API.
    # Assumes you have litellm installed and AWS creds in environment.
    return OpenAIChatCompletionClient(
        model="bedrock/apac.amazon.nova-pro-v1:0",
        api_key="not-used",
        base_url="http://localhost:4000",  # litellm proxy
    )


async def main():
    client = build_bedrock_client()
    planner = AssistantAgent(
        name="Planner",
        model_client=client,
        system_message=(
            "You are a planning agent. Break tasks into steps. "
            "When you are satisfied, say TERMINATE."
        ),
    )
    critic = AssistantAgent(
        name="Critic",
        model_client=client,
        system_message=(
            "You critique plans. Point out flaws, "
            "then let the Planner revise."
        ),
    )
    termination = TextMentionTermination("TERMINATE")
    team = RoundRobinGroupChat(
        [planner, critic],
        termination_condition=termination,
    )
    await team.run(
        task="Plan a rollout for a new CloudWatch alarm strategy."
    )

if __name__ == "__main__":
    asyncio.run(main())
