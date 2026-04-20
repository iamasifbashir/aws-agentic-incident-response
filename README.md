# AWS Agentic Incident Response
A multi-agent incident response system on AWS, built with the Strands
Agents SDK and deployed to Amazon Bedrock AgentCore Runtime.
## Status
Work in progress. Built as part of a 7-day learning sprint.
## Architecture
(Diagram coming in Day 1 evening.)
## Tech stack
- **Framework**: Strands Agents SDK
- **Runtime**: Amazon Bedrock AgentCore
- **Model**: Amazon Nova Pro (via APAC cross-region inference)
- **Multi-agent protocol**: A2A (Agent-to-Agent)
- **Observability**: OpenTelemetry via AgentCore Observability
- **ITSM integration**: Jira (coming Day 6)
## Running locally
(Instructions coming Day 2.)
## Repo structure
- `examples/` — incremental exercises, one per concept
- `src/` — the flagship project code (Day 4 onward)
- `docs/` — architecture notes and monitoring playbook
- `evals/` — evaluation datasets and results
