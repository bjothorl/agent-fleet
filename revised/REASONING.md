# Why revise the fleet prompts

Evidence from investigating the ignire fleet + custom-cursor LLM gateway (conversation spanning
2026-10-20 → 2026-10-22). Verbatim originals live in this folder; revised drafts in `revised/`.

## Executive summary

The fleet prompts optimize for **auditability and resume**, not **throughput**. On a representative
stretch (2026-10-21 12:00 UTC → 2026-10-22 afternoon), developer model-time was ~**18.6h**, of which
only ~**35%** was productive src/test read+write+verify. The rest was largely **STATUS/TASKS
paperwork**, **re-prefills**, and **measure loops** — behaviors the original prompts *require* or
fail to forbid.

Target: cut ~**⅓–½ of developer model-hours** without weakening Done-when discipline, by changing
who owns STATUS, shrinking launch context, and banning empty turns.

---

## Incident context (same period)

### Strata wedge (~00:41–07:36 local, 2026-10-22)

- Cursor/agent requests often omit `max_tokens`. Strata (since commit `656a8356`, 2026-09-26) treats
  unset max as **rest of context** (was previously default **1024**). Older Cursor dumps often sent
  `max_tokens: 4096`.
- A `Shell` tool-call generation ran toward `max ≈ 113813` tokens; stalled around **25k** with TCP
  backpressure (multi‑MB socket queues), GPU idle, cancel not fired (connection still open).
- Later chats hung for **12–150+ minutes** as HTTP 200 with null token usage — **no error in Cursor**.
- Restart of `strata-serve` cleared it (`BrokenPipeError` on old process).

**Prompt implication:** fleet seats need a finite completion budget; “unlimited rest of context” is
unsafe for tool-arg streams. Revised orchestrator documents this; gateway/client should also inject
`max_tokens` (out of band of these markdown files).

### Push bloat (side note)

Seven commits ahead of origin included ~**3295** `apps/gateway/debug/*.json` files — unrelated to
prompts, but shows debug dumps are large enough to recover skill text when `~/.cursor/agents` is gone.

---

## Timesheet (fleet roles)

**Window:** 2026-10-21 ~12:00 UTC → ~2026-10-22 13:30 UTC.  
**Method:** join `usage.jsonl` chat completions to gateway debug dumps; role from
`operating as the "fleet-…"`. Hours = Σ `durationMs`.

| Role | Calls | Model-hours | Share of joined | Notes |
|------|------:|------------:|----------------:|-------|
| **developer** | ~1222 | **~18.3** | **~58%** | Almost all `qwen` @ home |
| **orchestrator-parent** | ~406 | **~11.0** | **~35%** | Long parent thread + Task launches |
| **tech-lead** | ~222 | **~2.2** | **~7%** | |
| designer / tester / planner | fewer dumps | ~0.5–2h est. each | small | Weaker usage join; dump counts 226 / 111 / 62 |

Developer avg input **~94k tokens/call**. Context size p50 **~128 messages**, p90 **~285**.

Sampled developer dumps: **~4.5 Reads of `STATUS.md`** and **~2 Reads of `TASKS.md` per dump**.

---

## Developer time: read / write / shell

**Method:** attribute each matched usage call’s duration across tools in the **previous assistant
turn** (proportional to tool counts).

| Bucket | Hours | Share of ~18.6h |
|--------|------:|----------------:|
| WRITE | **8.1** | **43%** |
| READ | **6.9** | **37%** |
| SHELL | **3.2** | **17%** |
| Other | 0.5 | 3% |

### WRITE breakdown (the smoking gun)

| Target | Hours | Share of all dev |
|--------|------:|-----------------:|
| **`STATUS.md` / `TASKS.md` edits** | **7.3** | **39%** |
| `test/` edits | 0.4 | 2% |
| **`src/` edits** | **0.3** | **2%** |

Sampled meta writes: **443× STATUS**, **365× TASKS** — `Next action`, mark `doing`/`done`, Handoff,
Log lines.

### READ breakdown

| Target | Hours |
|--------|------:|
| test/ | 2.7 |
| src/ | 1.7 |
| STATUS + TASKS + DESIGN/ARCH/… | **1.5** |
| other | 0.9 |

### SHELL breakdown

| Kind | Hours |
|------|------:|
| verify (test/tsc) | 1.4 |
| **measure** (budget/length `node -e` farms) | **1.1** |
| other / meta | 0.7 |

**Productive loop** (src/test read + write + verify): ~**6.6h (35%)**.  
**Paperwork + measure:** ~**10h+**.

T55 afternoon Shell mix (raw counts): measure **295** / test **337** / other **597**.

---

## Iteration progress (for ETA context)

Execution order: T51 → T52 → T53 → T54 → T56 → **T55** → T57 → T58 → T59 → T60.

| Done | When (UTC+2) |
|------|----------------|
| T51–T53 | evening 2026-10-21 |
| T54 | 09:41 on 2026-10-22 |
| T56 | 11:58 on 2026-10-22 |
| Suite | **445/445** green @ 12:31 |

T55 (keymap + Enter) was in progress with test drafts and width measurement; two earlier passes were
**announcement-only** (no edits) — explicitly called out in launch prompts.

Productive daytime pace ~**1.2–2.3h per task**. Remaining five tasks ETA without downtime: ~**8–12h**.

---

## Mapping: original prompt → observed waste

| Original instruction | Observed effect |
|----------------------|-----------------|
| Shared contract: every role reads STATUS first + updates STATUS (phase, Next action, Log) | 4.5 STATUS reads/dump; **7.3h** STATUS/TASKS writes |
| Developer: read STATUS + TASKS + ARCH every task; update STATUS before anything else | Meta work ≫ `src/` edits (**0.3h**) |
| Orchestrator: subagents see no history — include full context in Task prompt | Multi‑kB launch prompts; ~94k avg input |
| Developer: one task; don’t batch | Safe but serial; no parallel disjoint tasks |
| Designer: HTML + screenshot + read-back loop | Correct for design; costly if re-entered mid-dev |
| Tester: do not fix failures | Extra full round-trips for typos |
| Auto-approve still “must be recorded” | Long decision/log prose while user asleep |
| *(missing)* finite `max_tokens` | Strata runaway / overnight wedge |
| *(missing)* must-edit rule | Announcement-only developer turns |
| *(missing)* measure-loop cap | Shell candidate farms on T55 |

Orchestrator-parent alone consumed **~35%** of joined model-hours — monitoring + fat relaunches +
summary-heavy parent threads.

---

## What the revised prompts change

### Orchestrator (`revised/fleet-orchestrator.SKILL.md`)

1. **STATUS ownership moves to orchestrator** — roles only flip task `doing`/`done` + task Handoff.
2. **≤80-line launch brief**; ban pasting full STATUS / Handoff novels into Task prompts.
3. **Empty-turn relaunch rule** for developer/tech-lead.
4. **Disjoint-file parallelism** allowed when safe.
5. Document **finite max_tokens** for local/unlimited upstreams; keep parent thread short.

### Developer (`revised/fleet-developer.md`)

1. Brief-first; **no full STATUS read** by default.
2. Read **one task section**, not whole TASKS.md.
3. **Edit-or-fail** within first substantive turn.
4. **No STATUS Next action / Log edits**.
5. Cap measure loops; prefer one helper script.

### Planner / Tech lead / Designer / Tester

- Brief-first reads; short Handoffs (≤15–20 lines).
- No STATUS Log ownership.
- Designer: screenshot loop scoped to **design phase**.
- Tester: **narrow fix-forward** for assertion typos; prefer Handoff checks over re-reading all docs.
- Tech lead: mark **parallel-safe** tasks; keep ARCHITECTURE skim-sized.

### Intentionally unchanged

- Phase order and gates (plan → design → architecture → developer → test).
- One-sitting task sizing and concrete `Done when`.
- Designer HTML-as-evidence (when designing).
- Tester evidence requirement (commands / screenshots).
- Never rewrite `REQUEST.md`.

---

## Expected savings (order of magnitude)

If STATUS/TASKS write storm drops by ~70%, measure loops by ~50%, and STATUS re-reads by ~50%:

| Pool (from split) | Rough save |
|-------------------|------------|
| write_fleet_meta 7.3h | ~5h |
| shell_measure 1.1h | ~0.5h |
| fleet doc reads 1.5h | ~0.7h |
| **Total** | **~6–8h per similar 18h developer stretch** |

Plus softer wins: fewer announcement-only relaunches, smaller orchestrator-parent context, lower
wedge risk with max_tokens policy.

---

## Out of band (not only markdown)

These prompt edits are necessary but not sufficient:

1. **Gateway or Cursor client:** default `max_tokens` (e.g. 4096–8192) for fleet seats.
2. **Strata:** stalled-SSE write timeout → cancel (see `docs/BUG_UNBOUNDED_MAX_TOKENS_STREAM_STALL.md`
   in the Strata repo).
3. **Optional:** `fleet/NEXT.md` (≤80 lines) maintained by orchestrator so agents never open full STATUS.
4. **Cursor:** trim injected `progress_reporting_instructions` on subagents if possible (not in these
   skill files, but present at runtime).

---

## File layout

```
docs/fleet-prompts/
  README.md                 # provenance of verbatim recovery
  REASONING.md              # this file
  fleet-orchestrator.SKILL.md
  fleet-planner.md
  fleet-designer.md
  fleet-tech-lead.md
  fleet-developer.md
  fleet-tester.md
  revised/                  # proposed replacements
    fleet-orchestrator.SKILL.md
    fleet-planner.md
    …
```

To adopt: copy `revised/*` over `~/.cursor/skills/fleet-orchestrator/SKILL.md` and
`~/.cursor/agents/fleet-*.md` (paths as used in the Oct 2026 ignire run).
