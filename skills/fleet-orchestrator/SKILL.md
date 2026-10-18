---
name: fleet-orchestrator
description: >-
  Runs a multi-role agent fleet (planner, designer, tech lead, developer, tester) as a resumable
  state machine over the fleet/ artifact folder. Use when the user wants to start a long-running
  coding epic, continue or resume fleet work, check fleet status, or asks which role should act next.
disable-model-invocation: true
---

# Fleet Orchestrator

Coordinates the five fleet roles. It does not do the role's work itself; it decides which role acts
next, enforces approval gates, and keeps `fleet/STATUS.md` current so a run survives across sessions.

## Shared contract

Every role follows the same rules. Enforce them:

1. Read `fleet/STATUS.md` before anything else.
2. Read the upstream artifacts named in its own agent prompt before writing.
3. Write only its own artifact file, plus a `Handoff` section listing inputs consumed and open
   questions.
4. Update `fleet/STATUS.md`: `phase`, `owner`, `Next action`, `Blockers`, and one `Log` line.

Two formatting rules the tooling depends on: frontmatter values must not carry inline comments, and a
task ID is the first token after `### ` in `TASKS.md`. Both were broken during the pilot run.

Never rewrite `fleet/REQUEST.md`. Corrections go into `PLAN.md` as a dated revision.

## Starting a run

If `fleet/STATUS.md` is at `phase: intake` and `REQUEST.md` is empty:

1. Capture the epic in `fleet/REQUEST.md`: goal, success criteria, out of scope, constraints. Ask the
   user for anything missing rather than guessing.
2. Set `pilot` to a short slug, `phase: plan`, `owner: orchestrator`.
3. Run the planner.

## Phase loop

Order is `plan` → `design` → `architecture` → `developer` → `test` → `done`.

For the current phase, launch the matching fleet subagent in the **foreground** via the Task tool or
`/fleet-planner`, `/fleet-designer`, `/fleet-tech-lead`, `/fleet-developer`, `/fleet-tester`. Include
in the task prompt: paths to `fleet/STATUS.md`, upstream artifacts, gate state from `STATUS.md`, and
any user constraints from this conversation. Subagents do not see chat history; do not paraphrase the
role from memory.

After a role returns, read its `Handoff`. If it raised open questions, surface them to the user
before advancing.

## Approval gates

Planner, designer, and tech lead each end with a gate. Stop and present a short checklist:

- What the role decided.
- The one or two decisions the user should confirm or challenge.
- `Next action` if approved.

Advance only when the user approves, or when the user previously said gates are auto-approved. Record
approval in the `approved` block of `STATUS.md`. A gate that was auto-approved must still be recorded,
so a later session knows it was not reviewed by a human.

Design may be skipped when the epic has no interface surface. Record that as `design: n/a` rather
than leaving the gate unmarked.

## Long-running work

The developer phase is where runs stall, so make it resumable:

- Work one `TASKS.md` item at a time. Check it off, then update `STATUS.md` before continuing.
- If a task is left `doing`, write a one-line note in `Next action` describing exactly where it
  stopped. That note is what a new session reads.
- Do not batch multiple tasks into one pass unless the user asks for it.

When the user says "continue" in a new session, read `STATUS.md` and `TASKS.md`, then resume at the
recorded task. Do not re-plan work that is already approved.

## Delegating to subagents

Use the Task tool only when isolation genuinely helps:

- `explore` before the tech lead sizes tasks, when the codebase is unfamiliar.
- `generalPurpose` for a single bounded task, with `TASKS.md` and `ARCHITECTURE.md` pasted into the
  prompt. Subagents cannot see the conversation, so include the full context they need.

Do not delegate planning, design, or approval decisions to background subagents. Those need the user
in the loop; fleet role agents run in the foreground at gates.

## Reporting

Lead with the phase and the next action. If blocked, say what was tried and what is needed. Keep it
short: the user is reading a status board, not a narrative.
