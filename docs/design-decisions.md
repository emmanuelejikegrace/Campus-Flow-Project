# Design Decisions

- **Dicts, not classes.** JSON-native; auditable by opening the file.
- **`assigned_to = None`** for unassigned. Empty string would be ambiguous.
- **Priority order is load-bearing.** Rules are first-match; reordering R2 and R3 would misclassify high-urgency low-impact tickets.
- **Numeric ID tie-break.** `T010` > `T002` numerically, but `<` as strings.
- **Corrupt JSON aborts startup.** Never silently erase user data.
- **IDs derived from `max()` on load.** Self-healing; no separate counter to drift.

# WHAT IS THE EXPECTED RETURN VALUE WHEN A TICKET IS CREATED, ASSIGNED, OR UPDATED

* When Created: Returns the new ticket's details, including its unique ID and initial status.

* When Assigned: Returns the updated ticket with the assigned user's ID or name.

* When Updated: Returns the ticket with the modified fields and current status.

* On failure: Raises an exception or returns a structured error explaining the problem.

# HOW CAN WE TEST BUSINESS LOGIC WITHOUT ASKING FOR INTERACTIVE INPUT INSIDE EACH TEST?

* By Separating business logic from user input: Keep input() and print() in the CLI layer.

* By Using function parameters: Pass test data directly to business functions.

* Bu Testing with pytest: Assert expected return values and errors without interactive input.

* Mock dependencies: Replace file operations or external services when necessary.
