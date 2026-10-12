# Campus-Flow-Project
a Python command-line ticket manager that records problems, prioritizes work, assigns responsibility, and tracks progress.

## Run
    python main.py

## Test
    python -m unittest discover -s tests -v

## Features
- F1 Create ticket (validated, auto-priority, unique ID)
- F2 List / view tickets
- F3 Assign to staff
- F4 Workflow: open → in_progress → resolved, with explicit reopen
- F5 Work queue (unresolved, critical → low, ID tie-break)
- F6 Reports (totals, by status, by priority)
- F7 JSON persistence with corrupt-file protection

## Data
Tickets persist to `data/tickets.json`. That file is gitignored.

# sha
fcbc843e82a96cc98e17df651695d13a9bd947ae