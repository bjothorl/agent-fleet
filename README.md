# Agent fleet

A five-role fleet for long-running coding work in Cursor: planner, designer, tech lead, developer,
tester. The orchestrator is a Cursor skill; role work runs through subagents in `.cursor/agents/`.
Durable state lives in `fleet/`, so a run survives across sessions.

## Roles

| Role | Invocation | Writes |
|------|------------|--------|
| Orchestrator | skill `@fleet-orchestrator` | `fleet/STATUS.md` |
| Planner | agent `/fleet-planner` | `fleet/PLAN.md`, draft `fleet/TASKS.md` |
| Designer | agent `/fleet-designer` | `fleet/DESIGN.md` |
| Tech lead | agent `/fleet-tech-lead` | `fleet/ARCHITECTURE.md`, refined `fleet/TASKS.md` |
| Developer | agent `/fleet-developer` | code, checks off `fleet/TASKS.md` |
| Tester | agent `/fleet-tester` | `fleet/TEST_REPORT.md`, follow-up tasks |

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
/fleet-developer Implement TASK-003 only
/fleet-tester Run a test pass on the completed tasks
```

## Copying the fleet into another project

Copy `.cursor/skills/fleet-orchestrator/`, `.cursor/agents/fleet-*.md` (five role agents), and the
`fleet/` folder into the target repo. For global use, copy the skill to `~/.cursor/skills/` and the
agent files to `~/.cursor/agents/`. Keep paths identical; everything references `fleet/` by path.

## Pilot epic

The fleet was dry-run on a small end-to-end epic in this repo: a stdlib Python CLI that validates
`fleet/STATUS.md` and prints the next phase. It is small enough that every role produced real output,
which is what exposed the handoff gaps now fixed in the agents. See `fleet/` for the artifacts from
that run.
