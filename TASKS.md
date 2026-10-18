# Tasks

Ordered work units. Tech lead sizes them; developer checks them off; tester adds follow-ups.

Rules:

- One task per sitting, roughly one to three files.
- Status is `todo`, `doing`, `done`, or `deferred`. Never leave `doing` across sessions without a note.
- Tester-added tasks are appended, never inserted into the middle of an approved sequence.

## Tasks

### TASK-001 — Frontmatter parser
Status: todo
Files: `fleetctl.py`
Depends on: none
Done when: `parse_frontmatter` returns top-level keys and the nested `approved` block for a valid
status file, and raises `StatusError` when the block is missing or unterminated.

### TASK-002 — Validation
Status: todo
Files: `fleetctl.py`
Depends on: TASK-001
Done when: `validate` returns one error string per problem for unknown phase, unapproved gate at a
later phase, empty `Next action`, and a task left `doing` without a note.

### TASK-003 — CLI
Status: todo
Files: `fleetctl.py`
Depends on: TASK-002
Done when: `python3 fleetctl.py` prints phase and next action, `--check` prints `ok` or one error per
line, `--status PATH` overrides the default, and exit codes are 0 or 1 with no stack trace.

### TASK-004 — Tests
Status: todo
Files: `tests/test_fleetctl.py`
Depends on: TASK-003
Done when: `python3 -m unittest discover -s tests` passes, covering a valid file, an unknown phase, an
unapproved gate, an empty next action, and a missing status file.
