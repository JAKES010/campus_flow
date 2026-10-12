"""Status lifecycle and work queue (Engineer B)."""
from .tickets import (
    PRIORITIES, STATUSES, WorkflowError, ValidationError,
    get_ticket, ticket_number,
)

# open -> in_progress -> resolved ; resolved -> open (explicit reopen only)
ALLOWED_TRANSITIONS = {
    "open": {"in_progress"},
    "in_progress": {"resolved"},
    "resolved": {"open"},
}


def normalize_status(status):
    if isinstance(status, str):
        cleaned = status.strip().lower().replace("-", "_").replace(" ", "_")
        if cleaned in STATUSES:
            return cleaned
    raise ValidationError(
        f"Invalid status {status!r}. Allowed: {', '.join(STATUSES)}."
    )


def change_status(tickets, ticket_id, new_status):
    ticket = get_ticket(tickets, ticket_id)
    new_status = normalize_status(new_status)
    current = ticket["status"]
    if new_status not in ALLOWED_TRANSITIONS[current]:
        raise WorkflowError(f"Cannot move {ticket['id']} from {current} to {new_status}.")
    if new_status == "in_progress" and not ticket["assigned_to"]:
        raise WorkflowError(
            f"{ticket['id']} is unassigned; assign it before starting work."
        )
    ticket["status"] = new_status
    return ticket


def reopen_ticket(tickets, ticket_id):
    ticket = get_ticket(tickets, ticket_id)
    if ticket["status"] != "resolved":
        raise WorkflowError(f"{ticket['id']} is not resolved, so it cannot be reopened.")
    return change_status(tickets, ticket_id, "open")


def work_queue(tickets):
    """Open tickets: critical -> high -> medium -> low, ties by numeric ID."""
    rank = {name: index for index, name in enumerate(PRIORITIES)}
    waiting = [t for t in tickets if t["status"] == "open"]
    return sorted(waiting, key=lambda t: (rank[t["priority"]], ticket_number(t["id"])))
