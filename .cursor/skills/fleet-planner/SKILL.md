---
name: fleet-planner
description: >-
  Defines scope, approach, milestones, and success criteria for a fleet epic, and drafts the first
  task list. Use when the fleet is at phase plan, when scope changes, or when the user asks for a
  plan or re-plan.
disable-model-invocation: true
---

# Fleet Planner

Produces `fleet/PLAN.md`. Does not design interfaces or pick implementation details, and does not
write code.

## Before writing

Read `fleet/STATUS.md` and `fleet/REQUEST.md`. If success criteria are missing or the scope is
ambiguous, ask the user rather than assuming.

## Plan contents

- **Approach**: the shape of the solution in plain language, and why it fits the request.
- **Milestones**: three to six checkpoints, each independently verifiable.
- **Risks and unknowns**: what could invalidate the approach, and what would settle it.
- **Out of scope**: restated from `REQUEST.md`, plus anything the plan deliberately excludes.

Keep it under 50 lines. A plan the user cannot read in a minute is not a plan.

## Drafting tasks

Append initial tasks to `fleet/TASKS.md` using the template there. Size them for one sitting, roughly
one to three files. Mark them `todo`. The tech lead will refine them; do not over-specify files you
have not read.

## Gate

Present to the user: the approach, the milestones, and the two decisions worth challenging. Wait for
approval before the fleet advances. Record approval in `STATUS.md`.

## Handoff

Append a `Handoff` section to `PLAN.md`: inputs consumed, open questions, and the recommended next
role.
