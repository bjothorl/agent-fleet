# Agent fleet

A five-role fleet for long-running coding work in Cursor: planner, designer, tech lead, developer,
tester. Roles are Cursor Skills, and the durable state lives in `fleet/`, so a run survives across
sessions.

## Roles

| Role | Skill | Writes |
|------|-------|--------|
| Orchestrator | `fleet-orchestrator` | `fleet/STATUS.md` |
| Planner | `fleet-planner` | `fleet/PLAN.md`, draft `fleet/TASKS.md` |
| Designer | `fleet-designer` | `fleet/DESIGN.md` |
| Tech lead | `fleet-tech-lead` | `fleet/ARCHITECTURE.md`, refined `fleet/TASKS.md` |
| Developer | `fleet-developer` | code, checks off `fleet/TASKS.md` |
| Tester | `fleet-tester` | `fleet/TEST_REPORT.md`, follow-up tasks |

Phase order is `plan` → `design` → `architecture` → `developer` → `test` → `done`. Planner, designer,
and tech lead stop at an approval gate before the fleet advances.

## Start a run

Open this repo in Cursor, then in an Agent chat:

```
@fleet-orchestrator Start a new epic: <what you want built>
```

The orchestrator captures the request in `fleet/REQUEST.md`, sets `fleet/STATUS.md` to `phase: plan`,
and runs the roles in order. Answer each gate with `approve` or `revise: <note>`.

## Resume a run

In a new chat, nothing else is needed:

```
@fleet-orchestrator Continue from fleet/STATUS.md
```

The orchestrator reads the status board and picks up at the recorded task. This is the whole point of
the artifact folder: chat memory ends, files do not.

## Run a single role

When you want manual control over one phase:

```
@fleet-developer Implement TASK-003 only
@fleet-tester Run a test pass on the completed tasks
```

## Copying the fleet into another project

Copy `.cursor/skills/fleet-*` and the `fleet/` folder into the target repo, or add this repo as a
submodule and point the skills at the artifacts. Keep the file names identical, because the skills
reference them by path.

## Pilot epic

The fleet was dry-run on a small end-to-end epic in this repo: a stdlib Python CLI that validates
`fleet/STATUS.md` and prints the next phase. It is small enough that every role produced real output,
which is what exposed the handoff gaps now fixed in the skills. See `fleet/` for the artifacts from
that run.
