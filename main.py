"""CampusFlow CLI entry point."""

from campusflow import storage, reports, workflow, tickets


MENU = """
===== CampusFlow =====
1. Create ticket
2. List all tickets
3. View one ticket
4. Assign ticket
5. Workflow (start / resolve / reopen)
6. Work queue
7. Reports
8. Save and exit
"""


def _print_ticket(t):
    print(f"  ID:            {t['id']}")
    print(f"  Title:         {t['title']}")
    print(f"  Category:      {t['category']}")
    print(f"  Urgency:       {t['urgency']}")
    print(f"  Affected:      {t['affected_users']}")
    print(f"  Priority:      {t['priority']}")
    print(f"  Status:        {t['status']}")
    print(f"  Assigned to:   {t['assigned_to']}")


def create_flow(tickets_list):
    print("\n-- Create ticket --")
    title = input("Title: ")
    category = input("Category (Network/Hardware/Software/Other): ")
    urgency = input("Urgency (low/medium/high): ")
    affected = input("Affected users: ")

    ticket, err = tickets.create_ticket(tickets_list, title, category, urgency, affected)
    if err:
        print(f"ERROR: {err}")
    else:
        print(f"Created {ticket['id']} (priority={ticket['priority']}).")


def list_flow(tickets_list):
    print("\n-- All tickets --")
    if not tickets_list:
        print("  (no tickets yet)")
        return
    for t in tickets_list:
        print(f"  {t['id']} | {t['priority']:8} | {t['status']:11} | {t['title']}")


def view_flow(tickets_list):
    tid = input("\nTicket ID to view: ").strip().upper()
    t = tickets.find_by_id(tickets_list, tid)
    if t is None:
        print(f"Unknown ticket ID: {tid}")
        return
    _print_ticket(t)


def assign_flow(tickets_list):
    tid = input("\nTicket ID to assign: ").strip().upper()
    name = input("Staff name: ")
    ok, msg = workflow.assign(tickets_list, tid, name)
    print(msg)


def workflow_flow(tickets_list):
    print("\n-- Workflow --")
    print("1. Start progress   2. Resolve   3. Reopen")
    choice = input("> ").strip()
    tid = input("Ticket ID: ").strip().upper()

    if choice == "1":
        ok, msg = workflow.start_progress(tickets_list, tid)
    elif choice == "2":
        ok, msg = workflow.resolve(tickets_list, tid)
    elif choice == "3":
        ok, msg = workflow.reopen(tickets_list, tid)
    else:
        print("Unknown workflow option.")
        return
    print(msg)


def queue_flow(tickets_list):
    print("\n-- Work queue (unresolved, priority order) --")
    queue = reports.work_queue(tickets_list)
    if not queue:
        print("  (nothing pending)")
        return
    for t in queue:
        owner = t["assigned_to"] or "UNASSIGNED"
        print(f"  {t['id']} | {t['priority']:8} | {t['status']:11} | {owner:12} | {t['title']}")


def report_flow(tickets_list):
    print("\n-- Reports --")
    total, by_status, by_priority = reports.summary(tickets_list)
    print(f"Total tickets: {total}")
    print("By status:")
    for s, n in by_status.items():
        print(f"  {s:12} {n}")
    print("By priority:")
    for p, n in by_priority.items():
        print(f"  {p:12} {n}")


def main():
    try:
        tickets_list = storage.load()
    except RuntimeError as e:
        print(f"FATAL: {e}")
        return

    while True:
        print(MENU)
        choice = input("Choice: ").strip()

        if choice == "1":
            create_flow(tickets_list)
        elif choice == "2":
            list_flow(tickets_list)
        elif choice == "3":
            view_flow(tickets_list)
        elif choice == "4":
            assign_flow(tickets_list)
        elif choice == "5":
            workflow_flow(tickets_list)
        elif choice == "6":
            queue_flow(tickets_list)
        elif choice == "7":
            report_flow(tickets_list)
        elif choice == "8":
            storage.save(tickets_list)
            print("Saved. Goodbye.")
            return
        else:
            print("Unknown option.")

if __name__ == "__main__":
    main()
