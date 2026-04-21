# Example 02 -- AWS Cost Investigator

A three-tool Strands agent that investigates AWS cost anomalies and
drafts formatted remediation notes.
## What it does

Given a natural-language question about recent spend, the agent:
1. Queries Cost Explorer for service-level spend with vs-previous-window deltas.
2. Queries CloudWatch alarms for services of interest.
3. Produces a markdown-formatted remediation note with severity and action.

## Tools
- **get_cost_by_service** -- Cost Explorer aggregate by SERVICE dimension,
 daily or monthly granularity, with window-over-window comparison.
- **get_cloudwatch_alarm_state** -- Lists current alarm states with
 optional name filtering; results sorted ALARM first.
- **draft_remediation_note** -- Pure formatting tool for consistent output.

## Design decisions
- **Summarised tool outputs.** Both AWS tools return summaries, not raw
 API responses. Keeps context window usage low and the agent focused.
- **Explicit severity ladder in the system prompt.** Removes guesswork
 from a subjective judgement.
- **No write operations.** All tools are read-only. The agent can
 diagnose and recommend; humans decide.
- **Regional nuance.** Cost Explorer forced to us-east-1; everything
 else runs in ap-southeast-2.

## Model
Amazon Nova Pro via the APAC Cross-Region Inference Profile
(`apac.amazon.nova-pro-v1:0`). Model is swappable to
`au.anthropic.claude-sonnet-4-6` with a one-line change.

## Running it
```
python -m examples.02_cost_investigator.agent
```

## Sample transcript
See `transcript.md` for a recorded run against a real AWS account.