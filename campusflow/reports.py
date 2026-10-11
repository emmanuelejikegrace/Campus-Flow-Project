"""Reporting: totals and breakdowns by status and priority."""

from campusflow.tickets import STATUSES


PRIORITY_ORDER = ("critical", "high", "medium", "low")


def summary(tickets):
    """Return (total, by_status, by_priority)."""
    by_status = {s: 0 for s in STATUSES}
    by_priority = {p: 0 for p in PRIORITY_ORDER}

    for t in tickets:
        if t["status"] in by_status:
            by_status[t["status"]] += 1
        if t["priority"] in by_priority:
            by_priority[t["priority"]] += 1

    return len(tickets), by_status, by_priority


def work_queue(tickets):
    """Unresolved tickets sorted by priority then numeric ID."""
    rank = {p: i for i, p in enumerate(PRIORITY_ORDER)}
    active = [t for t in tickets if t["status"] != "resolved"]
    return sorted(active, key=lambda t: (rank[t["priority"]], int(t["id"][1:])))