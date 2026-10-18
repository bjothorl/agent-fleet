# Request

Written by the orchestrator at intake. Treat as immutable once a run is underway; changes go in
`PLAN.md` as revisions, not by rewriting this file.

## Epic

Add `fleetctl.py`: a command-line tool that reads `fleet/STATUS.md`, validates it against the fleet
contract, and prints the phase and the next action.

## Success criteria

- Prints the current phase and `Next action` from `fleet/STATUS.md`.
- Reports concrete validation errors rather than a generic failure.
- Exits nonzero when the status file is invalid, so it can be used in CI.
- Uses only the Python standard library.

## Out of scope

- Writing or mutating artifacts. The tool is read-only.
- Parsing `TASKS.md` task bodies beyond the status check for a task left `doing`.
- Any dependency install, packaging, or publishing.

## Constraints

- Python 3.13 is available; `pyyaml` is not installed, so frontmatter parsing must not depend on it.
- Keep the tool small enough that a single developer pass can finish it.
