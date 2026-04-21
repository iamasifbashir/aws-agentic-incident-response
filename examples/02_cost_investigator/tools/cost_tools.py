"""Cost Explorer tools for the investigator agent."""
from datetime import date, timedelta
import boto3
from dateutil.utils import today
from strands import tool


@tool
def get_cost_by_service(
    days: int = 7,
    top_n: int = 5,
    granularity: str = "DAILY",
) -> str:
    """Get AWS spend grouped by service over a recent window.

    Use this tool as the starting point for any cost investigation. It
    returns the top N services by total spend over the last N days, so
    you can quickly see which services drove the bill. Use a small top_n
    (5 to 10) to keep the response focused.
    
    Args:
        days: Size of the lookback window in days (1 to 90). Default 7.
        top_n: How many top services to return (1 to 20). Default 5.
        granularity: "DAILY" or "MONTHLY". Use DAILY for anomaly
            investigation, MONTHLY for trend analysis. Default DAILY.
    
    Returns:
        A human-readable summary of the top services by spend, with
        totals and a comparison to the previous equivalent window.
    """
    if not 1 <= days <= 90:
        return "Error: days must be between 1 and 90."
    if not 1 <= top_n <= 20:
        return "Error: top_n must be between 1 and 20."
    if granularity not in ("DAILY", "MONTHLY"):
        return "Error: granularity must be DAILY or MONTHLY."
    
    ce = boto3.client("ce", region_name="us-east-1")
    
    today = date.today()
    start = today - timedelta(days=days)
    prev_start = start - timedelta(days=days)

    try:
        current = ce.get_cost_and_usage(
            TimePeriod={"Start": start.isoformat(), "End": today.isoformat()},
            Granularity=granularity,
            Metrics=["UnblendedCost"],
            GroupBy=[{"Type": "DIMENSION", "Key": "SERVICE"}],
        )
        previous = ce.get_cost_and_usage(
            TimePeriod={"Start": prev_start.isoformat(),
                        "End": start.isoformat()},
            Granularity=granularity,
            Metrics=["UnblendedCost"],
            GroupBy=[{"Type": "DIMENSION", "Key": "SERVICE"}],
        )
    except ce.exceptions.DataUnavailableException:
        return ("Cost Explorer has no data for this account yet. "
            "It takes up to 24 hours to populate after enablement.")
    except Exception as e:
        return f"Cost Explorer API error: {type(e).__name__}: {e}"
    
    totals = _sum_by_service(current)
    prev_totals = _sum_by_service(previous)

    ranked = sorted(totals.items(), key=lambda kv: kv[1], reverse=True)[:top_n]
    if not ranked:
        return f"No spend recorded in the last {days} days."
    
    lines = [f"Top {len(ranked)} services by spend, "
        f"last {days} days (vs previous {days} days):"]
    for service, cost in ranked:
        prev = prev_totals.get(service, 0.0)
        delta_pct = ((cost - prev) / prev * 100) if prev > 0 else None
        delta_str = (f"{delta_pct:+.0f}%" if delta_pct is not None
        else "new (no prior spend)")
        lines.append(f" - {service}: ${cost:.2f} ({delta_str})")

    total = sum(totals.values())
    prev_total = sum(prev_totals.values())
    lines.append(f"Total (all services): ${total:.2f} "
        f"vs ${prev_total:.2f} previous window.")
    return "\n".join(lines)

def _sum_by_service(response: dict) -> dict:
    """Flatten a GetCostAndUsage response into {service: total_cost}."""
    out: dict = {}
    for period in response.get("ResultsByTime", []):
        for group in period.get("Groups", []):
            service = group["Keys"][0]
            amount = float(group["Metrics"]["UnblendedCost"]["Amount"])
            out[service] = out.get(service, 0.0) + amount
    return out
