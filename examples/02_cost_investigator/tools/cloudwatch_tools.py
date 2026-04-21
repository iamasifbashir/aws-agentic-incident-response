"""CloudWatch alarm tools for the investigator agent."""

import boto3
from strands import tool

@tool
def get_cloudwatch_alarm_state(
    service_filter: str = "",
    region: str = "ap-southeast-2",
) -> str:
    """Get the current state of CloudWatch alarms, optionally filtered.

    Use this tool after get_cost_by_service has identified a service
    worth investigating. It returns the current state of alarms in the
    given region, with optional name-based filtering.

    Args:
        service_filter: A substring to match against alarm names
            (case-insensitive). Example: "RDS" will match
            "prod-rds-cpu-high". Leave empty to see all alarms.
        region: AWS region to query. Default "ap-southeast-2".
    
    Returns:
    A human-readable summary of matching alarms with their current
    state, or a note that no alarms match.
    """
    try:
        cw = boto3.client("cloudwatch", region_name=region)
        response = cw.describe_alarms(MaxRecords=100)
    except Exception as e:
        return f"CloudWatch API error: {type(e).__name__}: {e}"
    
    alarms = response.get("MetricAlarms", [])
    if service_filter:
        needle = service_filter.lower()
        alarms = [a for a in alarms if needle in a["AlarmName"].lower()]
    
    if not alarms:
        filt = f" matching '{service_filter}'" if service_filter else ""
        return f"No alarms found{filt} in region {region}."
    
    # Sort: ALARM first, then INSUFFICIENT_DATA, then OK
    state_order = {"ALARM": 0, "INSUFFICIENT_DATA": 1, "OK": 2}
    alarms.sort(key=lambda a: state_order.get(a["StateValue"], 99))
    
    lines = [f"Found {len(alarms)} alarm(s) in {region}:"]
    for a in alarms[:20]:  # cap for context safety
        reason = a.get('StateReason', 'no reason given')[:80]
        lines.append(f" [{a['StateValue']}] {a['AlarmName']} -- {reason}")
    if len(alarms) > 20:
        lines.append(f" ... and {len(alarms) - 20} more (not shown).")
    return "\n".join(lines)
