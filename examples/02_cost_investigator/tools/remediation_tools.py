"""Remediation note drafting tool."""
from datetime import datetime
from strands import tool


@tool
def draft_remediation_note(
    finding: str,
    severity: str = "medium",
    suggested_action: str = "",
) -> str:
    """Draft a formatted remediation note for a cost or operational finding.

    Use this tool ONLY after you have gathered enough evidence from the
    cost and alarm tools to state a finding clearly. The note will be
    included in the final answer and should read like something a human
    engineer would send to their team.
    
    Args:
        finding: A one-to-two sentence description of what was observed
            and why it matters. Plain English, no jargon.
        severity: One of "low", "medium", "high", "critical". Default
            "medium". Use "high" or "critical" only for things that are
            clearly urgent (production outage, major cost anomaly).
        suggested_action: Optional concrete next step. If you don't have
            a specific action to recommend, leave blank -- the note will
            suggest human review.
    
    Returns:
        A markdown-formatted remediation note, ready to paste into a
        ticket or Slack message.
    """
    valid_sev = {"low", "medium", "high", "critical"}
    if severity not in valid_sev:
        severity = "medium"
    
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    sev_tag = {"low": "", "medium": "", "high": "[!]", "critical": "[!!]"}
    tag = sev_tag.get(severity, "")
    
    if suggested_action:
        action_block = f"**Suggested action:** {suggested_action}"
    else:
        action_block = ("**Suggested action:** Recommend human review to "
                    "confirm and decide on remediation.")
    
    return (
        f"## Remediation Note {tag}\n"
        f"- Severity: **{severity.upper()}**\n"
        f"- Timestamp: {timestamp}\n"
        f"- Source: AWS Cost Investigator agent\n\n"
        f"**Finding:** {finding}\n\n"
        f"{action_block}\n"
    )
