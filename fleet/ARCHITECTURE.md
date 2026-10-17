# Architecture

Tech lead output. The developer implements against this file, so it must name real files and real
boundaries.

## Existing shape

The repo is documentation and skills only: `README.md`, `fleet/` artifacts, and
`.cursor/skills/fleet-*`. There is no code, no package manifest, and no test runner. Python 3.13 is
available at `/usr/bin/python3`; `pyyaml` is not installed.

## Chosen design

Two files.

- `fleetctl.py` — one module, four functions:
  - `parse_frontmatter(text)` returns a dict of top-level keys, with `approved` as a nested dict. It
    requires the block to open and close with `---` at column 0.
  - `read_status(path)` returns the parsed frontmatter and the body, or raises a `StatusError` with a
    message matching the design contract.
  - `validate(frontmatter, body, tasks_path)` returns a list of error strings. It checks the phase
    against `PHASES`, gate approval against the current phase, and `Next action` in the body.
  - `main(argv)` handles `--check`, `--status`, and the default print mode, and returns the exit code.
- `tests/test_fleetctl.py` — stdlib `unittest`, using `tempfile` for fixture status files so the tests
  do not depend on the live `fleet/STATUS.md`.

`PHASES` is the single source of truth for order, shared by validation and the gate check. No CLI
framework, no classes, no config file.

The gate check needs the phase order, so it lives in `validate` rather than in the parser. Keeping the
parser dumb and the validator opinionated is what makes both testable separately.

## Rejected alternatives

- **`pyyaml` for frontmatter**: not installed, and the key set is fixed. A dependency for five keys is
  not worth it.
- **Reading `TASKS.md` for the `doing` check**: kept, because it is a three-line scan and the fleet
  contract depends on it. It is skipped when `TASKS.md` is absent.
- **JSON output**: no consumer needs it yet.

## Handoff

Inputs consumed: `PLAN.md`, `DESIGN.md`
Open questions: none.
First task to execute: TASK-001.
