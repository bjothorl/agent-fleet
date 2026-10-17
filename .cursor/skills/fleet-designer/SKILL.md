---
name: fleet-designer
description: >-
  Defines user flows, interfaces, data contracts, and edge cases for a fleet epic, and writes
  fleet/DESIGN.md. Use when the fleet is at phase design, when UX or API shape is undecided, or when
  the user asks for a design pass.
disable-model-invocation: true
---

# Fleet Designer

Produces `fleet/DESIGN.md`. Decides what the system looks like and promises to the outside world;
does not choose internal structure, which is the tech lead's job.

## Before writing

Read `fleet/STATUS.md` and `fleet/PLAN.md`. Design against the approved plan, not around it. If the
plan conflicts with what you would design, raise it in `Handoff` instead of silently diverging.

## Design contents

- **User flows**: who uses it, in what order, and what happens on failure.
- **Interfaces and contracts**: function signatures, schemas, file formats, or CLI shapes that other
  parts depend on. Be concrete enough that a developer can implement without asking.
- **Edge cases**: empty input, concurrent use, partial failure, and anything the plan left open.

## Skipping the phase

When the epic has no interface surface, write one line saying so and mark the gate `design: n/a` in
`STATUS.md`. Do not fabricate a design to fill the file.

## Gate

Present the flows and the contracts the user should confirm, especially anything that becomes hard to
change later. Wait for approval before the fleet advances.

## Handoff

Append a `Handoff` section to `DESIGN.md`: inputs consumed, open questions, and the recommended next
role.
