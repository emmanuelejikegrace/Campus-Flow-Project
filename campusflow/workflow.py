"""Ticket assignment and workflow transitions."""


def assign(tickets, ticket_id, staff_name):
    """Assign a ticket to a non-empty staff name. Returns (ok, message)."""
    from campusflow.tickets import find_by_id

    ticket = find_by_id(tickets, ticket_id)
    if ticket is None:
        return False, f"Unknown ticket ID: {ticket_id}"

    name = (staff_name or "").strip()
    if not name:
        return False, "Staff name cannot be blank."

    ticket["assigned_to"] = name
    return True, f"{ticket['id']} assigned to {name}."


def start_progress(tickets, ticket_id):
    """open -> in_progress, only if assigned. Returns (ok, message)."""
    from campusflow.tickets import find_by_id

    ticket = find_by_id(tickets, ticket_id)
    if ticket is None:
        return False, f"Unknown ticket ID: {ticket_id}"

    if ticket["assigned_to"] is None:
        return False, "Cannot start an unassigned ticket."
    if ticket["status"] != "open":
        return False, f"Cannot start from status '{ticket['status']}'."

    ticket["status"] = "in_progress"
    return True, f"{ticket['id']} is now in_progress."


def resolve(tickets, ticket_id):
    """in_progress -> resolved. Returns (ok, message)."""
    from campusflow.tickets import find_by_id

    ticket = find_by_id(tickets, ticket_id)
    if ticket is None:
        return False, f"Unknown ticket ID: {ticket_id}"
    if ticket["status"] != "in_progress":
        return False, "Only in_progress tickets can be resolved."

    ticket["status"] = "resolved"
    return True, f"{ticket['id']} is now resolved."


def reopen(tickets, ticket_id):
    """resolved -> open, explicit reopen. Returns (ok, message)."""
    from campusflow.tickets import find_by_id

    ticket = find_by_id(tickets, ticket_id)
    if ticket is None:
        return False, f"Unknown ticket ID: {ticket_id}"
    if ticket["status"] != "resolved":
        return False, "Only resolved tickets can be reopened."

    ticket["status"] = "open"
    return True, f"{ticket['id']} reopened."