---

## name: fleet-orchestrator
description: >-
  Runs a multi-role agent fleet (planner, designer, tech lead, developer, tester) as a resumable
  state machine over the fleet/ artifact folder. Use when the user wants to start a long-running
  coding epic, continue or resume fleet work, check fleet status, or asks which role should act next.
disable-model-invocation: true

# Fleet Orchestrator

Coordinates the five fleet roles. It does not do the role's work itself; it decides which role acts
next, enforces approval gates, and keeps `fleet/STATUS.md` current so a run survives across sessions.

## Shared contract

Every role follows the same rules. Enforce them:

1. **Prefer the launch brief over re-reading STATUS.** The orchestrator pastes an ≤80-line brief

   (frontmatter, `Next action`, active task id, blockers that apply, paths). Roles may open the full
    `fleet/STATUS.md` only when the brief is missing or they hit a blocker.
2. Read the upstream artifacts named in the role prompt **only as needed** for that phase (see each

   agent file). Do not re-read the entire fleet folder every turn.
3. Write only the role's own artifact, plus a short `Handoff`.
4. **STATUS ownership:** the **orchestrator** updates `phase`, `owner`, `Next action`, `Blockers`, and

   Log lines after a role returns. Roles may only: (a) set their task line in `TASKS.md` to `doing` /
    `done` / `deferred`, and (b) append a `Handoff` under that task. They do not rewrite `Next action`
    or append Log essays mid-task.

Two formatting rules the tooling depends on: frontmatter values must not carry inline comments, and a
task ID is the first token after `###`  in `TASKS.md`.

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
`/fleet-planner`, `/fleet-designer`, `/fleet-tech-lead`, `/fleet-developer`, `/fleet-tester`.

### Task prompt template (keep short)

Subagents do not see chat history. Include **only**:

1. Role invocation (which agent file to follow).
2. The ≤80-line STATUS brief (or path + "read brief section only").
3. Exact task id / phase goal in one paragraph.
4. Paths to the 1–3 upstream files that role must read (not full pastes of Handoffs).
5. Gate mode: `human` or `auto-approved YYYY-MM-DD, NOT reviewed by a human`.
6. Constraints unique to this launch (file allowlist, "do not start Txx").

Do **not** paste prior Handoffs in full, full `TASKS.md`, or multi-thousand-line STATUS excerpts.

After a role returns, read its `Handoff`. Update STATUS once. If it raised open questions, surface
them to the user before advancing (unless auto-approved, then record the decision in one Log line).

## Approval gates

Planner, designer, and tech lead each end with a gate. Stop and present a short checklist:

- What the role decided.
- The one or two decisions the user should confirm or challenge.
- `Next action` if approved.

Advance only when the user approves, or when the user previously said gates are auto-approved. Record
approval in the `approved` block of `STATUS.md` (one line if auto-approved).

Design may be skipped when the epic has no interface surface. Record that as `design: n/a`.

## Long-running work

The developer phase is where runs stall, so make it resumable:

- Work one `TASKS.md` item at a time unless the user asks to batch **and** tasks touch disjoint files.
- Prefer parallel Task launches only for disjoint file sets (never two writers on `App.tsx`).
- If a task is left `doing`, set `Next action` to one line: task id + where it stopped.
- **Empty-turn rule:** if a developer/tech-lead returns with no file edits under `src/` or `test/`
(and no explicit `blocked` Handoff), relaunch once with "edit or mark blocked — no announcement-only
turns."

When the user says "continue" in a new session, read `STATUS.md` and resume at the recorded task. Do
not re-plan approved work.

When launching seats that talk to a local or unlimited-context upstream:

- Prefer a finite completion budget (e.g. pass `max_tokens` in the client config, typically 4096–8192).
- Do not rely on "rest of context" as the output cap — that enables multi-hour tool-arg runaways.

Keep the parent orchestrator thread short: do not mirror subagent tool traces into the parent; summarize
in STATUS Log only.

## Delegating to subagents

Use the Task tool when isolation helps:

- `explore` before the tech lead sizes tasks, when the codebase is unfamiliar.
- Fleet role agents in the foreground at gates.
- `generalPurpose` only for a single bounded task, with paths (not full file dumps) in the prompt.

Do not delegate planning, design, or approval decisions to background subagents.

## Reporting

Lead with the phase and the next action. If blocked, say what was tried and what is needed. Keep it
short: the user is reading a status board, not a narrative.
