# Design

Designer output. Skip this phase only when the epic has no user-facing or interface surface, and say
so explicitly here rather than leaving the file empty.

## User flows

The tool is run by a person checking where a run stands, or by CI as a guard.

1. Developer or orchestrator opens a new session.
2. `python3 fleetctl.py` prints the phase and the next action, so the reader knows where to resume.
3. CI runs `python3 fleetctl.py --check`. A nonzero exit means `fleet/STATUS.md` drifted from the
   contract, and the output names the problem.

On failure, the tool prints one line per problem and exits nonzero. It never prints a stack trace.

## Interfaces and contracts

```
usage: fleetctl.py [--check] [--status PATH]
```

- Default output, valid file:

  ```
  phase: developer
  next action: implement TASK-003
  ```

- `--check` prints `ok` on success, or one `error: <problem>` line per problem. Exit `0` when clean,
  `1` when not.
- `--status PATH` overrides the default `fleet/STATUS.md`, which is what makes the tool testable.

Recognised frontmatter keys: `phase`, `pilot`, `owner`, `gates`, `approved`. `approved` is a nested
block of `plan`, `design`, `architecture`, each `true`, `false`, or `n/a`.

Valid phases, in order: `intake`, `plan`, `design`, `architecture`, `developer`, `test`, `done`.

## Edge cases

- Missing `fleet/STATUS.md`: `error: status file not found`, exit 1.
- Unknown phase value: `error: unknown phase "<value>"`, exit 1.
- Frontmatter block missing or unterminated: `error: missing or unterminated frontmatter`, exit 1.
- A gate marked `n/a` is valid; a gate left `false` while the phase is past it is `error: gate <name>
  not approved at phase <phase>`.
- `Status: doing` in `TASKS.md` with no note on the same block: `error: task <id> left doing without a
  note`.
- Empty `Next action`: `error: Next action is empty`.

## Handoff

Inputs consumed: `PLAN.md`
Open questions: whether gate-order errors should be warnings instead of errors. Chosen as errors,
because the fleet contract says gates must be recorded before advancing.
Recommended next role: tech lead.
