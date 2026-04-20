"""
Hello-world Strands agent.
Uses Amazon Nova Pro via the APAC cross-region inference profile.
"""
from strands import Agent
from strands.models import BedrockModel
from strands_tools import calculator


def main() -> None:
    model = BedrockModel(
        model_id="apac.amazon.nova-pro-v1:0",
        region_name="ap-southeast-2",
        temperature=0.3,
        streaming=True,
    )
    agent = Agent(
        model=model,
        tools=[calculator],
        system_prompt=(
            "You are a helpful assistant. When a user asks a "
            "math question, use the calculator tool rather than "
            "computing the answer yourself."
        ),
    )
    result = agent("What is the square root of 1764, and what is "
                   "that number plus 100?")
    print("\n=== Final answer ===")
    print(result)


if __name__ == "__main__":
    main()
