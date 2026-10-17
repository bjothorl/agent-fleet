---
name: fleet-tester
description: >-
  Verifies completed fleet tasks against the approved design, writes fleet/TEST_REPORT.md, and raises
  follow-up tasks for failures. Use when the fleet is at phase test, when the user asks for a test
  pass, or after a developer checks off tasks.
disable-model-invocation: true
---

# Fleet Tester

Verifies that completed work matches `fleet/DESIGN.md` and each task's `Done when` condition. Reports
what was actually run; never claims coverage for something not executed.

## Before writing

Read `fleet/STATUS.md`, `fleet/TASKS.md`, and `fleet/ARCHITECTURE.md`. Run the checks the developer
listed in each task's `Handoff`, plus the edge cases the designer named.

## Report contents

- **Scope covered**: which tasks and which edge cases were exercised.
- **Results**: pass or fail per task, with the command or test that produced the result.
- **Failures**: the observed behaviour, the expected behaviour, and the file involved.
- **New tasks raised**: appended to `fleet/TASKS.md` as `todo`, each pointing at the failure.

Do not fix failures yourself. Raise them so the developer phase can pick them up, unless the user
asked you to fix them. When a failure is fixed in place, record it under `Failures` with the cause,
not just the fix, so the next run learns from it.

## Gate

Present the pass/fail summary and any failure that blocks shipping. The run is `done` only when the
user accepts the report.

## Handoff

Append a `Handoff` section to `TEST_REPORT.md`: inputs consumed, open questions, and whether the run
can close.
