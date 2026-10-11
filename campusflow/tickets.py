"""Ticket creation, validation, priority calculation, and ID generation."""

CATEGORIES = ("Network", "Hardware", "Software", "Other")
URGENCIES = ("low", "medium", "high")
STATUSES = ("open", "in_progress", "resolved")


def normalize_category(raw):
    """Return canonical category or None if invalid."""
    if raw is None:
        return None
    cleaned = raw.strip().lower()
    for c in CATEGORIES:
        if c.lower() == cleaned:
            return c
    return None


def normalize_urgency(raw):
    """Return canonical urgency or None if invalid."""
    if raw is None:
        return None
    cleaned = raw.strip().lower()
    return cleaned if cleaned in URGENCIES else None


def parse_affected_users(raw):
    """Return positive int or None if invalid.

    Rejects: blank, non-numeric text, decimals, zero, negatives.
    """
    if raw is None:
        return None
    text = str(raw).strip()
    if text == "":
        return None
    try:
        value = int(text)
    except ValueError:
        return None
    if value <= 0:
        return None
    return value


def calculate_priority(urgency, affected_users):
    """Ordered, first-match-wins priority calculation."""
    if urgency == "high" and affected_users >= 10:
        return "critical"
    if urgency == "high" or affected_users >= 10:
        return "high"
    if urgency == "medium" or affected_users >= 3:
        return "medium"
    return "low"


def next_id(tickets):
    """Generate the next unique ticket ID (T001, T002, ...)."""
    if not tickets:
        return "T001"
    highest = max(int(t["id"][1:]) for t in tickets)
    return f"T{highest + 1:03d}"


def find_by_id(tickets, ticket_id):
    """Return the ticket dict or None."""
    if ticket_id is None:
        return None
    needle = ticket_id.strip().upper()
    for t in tickets:
        if t["id"] == needle:
            return t
    return None


def create_ticket(tickets, title, category_raw, urgency_raw, affected_raw):
    """Validate inputs and append a new ticket. Returns (ticket, error)."""
    title = (title or "").strip()
    if not title:
        return None, "Title must not be blank."

    category = normalize_category(category_raw)
    if category is None:
        return None, f"Category must be one of: {', '.join(CATEGORIES)}"

    urgency = normalize_urgency(urgency_raw)
    if urgency is None:
        return None, f"Urgency must be one of: {', '.join(URGENCIES)}"

    affected = parse_affected_users(affected_raw)
    if affected is None:
        return None, "affected_users must be a positive whole number."

    ticket = {
        "id": next_id(tickets),
        "title": title,
        "category": category,
        "urgency": urgency,
        "affected_users": affected,
        "priority": calculate_priority(urgency, affected),
        "status": "open",
        "assigned_to": None,
    }
    tickets.append(ticket)
    return ticket, None