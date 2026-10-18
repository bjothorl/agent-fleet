# Plan

Planner output. One plan per epic; append revisions below rather than replacing history.

## Approach

A single-file stdlib script, `fleetctl.py`. It parses the YAML frontmatter of `fleet/STATUS.md` with a
small hand-written parser (no `pyyaml` in this environment), checks the phase against the known phase
order, and prints the phase plus `Next action`. Validation problems are reported as individual lines
so a failure in CI says what is wrong, not just that something is wrong.

The parser is deliberately narrow: it handles the keys `STATUS.md` actually contains. A general YAML
implementation is not worth the complexity here.

## Milestones

1. Frontmatter parser returns the known fields for a valid file.
2. Phase validation against the phase order, with a clear error for an unknown phase.
3. Output mode: phase and next action printed to stdout.
4. `--check` mode: validation only, nonzero exit on any problem.
5. Tests covering valid, invalid, and missing-file cases.

## Risks and unknowns

- Hand-rolled frontmatter parsing can drift if `STATUS.md` gains nested fields. Settled by keeping the
  parser to the documented keys and testing the nested `approved` block.
- A `doing` task with no note is a contract violation the tool can detect, but only if `TASKS.md` is
  read. Settled by limiting the check to the status file plus a simple scan for `Status: doing`.

## Out of scope

Read-only tool, no artifact mutation, no third-party dependencies.

## Handoff

Inputs consumed: `REQUEST.md`
Open questions: whether `--check` should also verify that every approved gate has a matching phase
history. Deferred to the tech lead.
Recommended next role: designer.
