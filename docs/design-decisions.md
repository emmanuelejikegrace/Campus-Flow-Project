# Design Decisions

- **Dicts, not classes.** JSON-native; auditable by opening the file.
- **`assigned_to = None`** for unassigned. Empty string would be ambiguous.
- **Priority order is load-bearing.** Rules are first-match; reordering R2 and R3 would misclassify high-urgency low-impact tickets.
- **Numeric ID tie-break.** `T010` > `T002` numerically, but `<` as strings.
- **Corrupt JSON aborts startup.** Never silently erase user data.
- **IDs derived from `max()` on load.** Self-healing; no separate counter to drift.