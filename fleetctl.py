#!/usr/bin/env python3
"""Read fleet/STATUS.md, validate it against the fleet contract, print the next action."""

import argparse
import sys
from pathlib import Path

PHASES = ["intake", "plan", "design", "architecture", "developer", "test", "done"]
GATES = ["plan", "design", "architecture"]


class StatusError(Exception):
    pass


def parse_frontmatter(text):
    """Return top-level frontmatter keys, with `approved` as a nested dict."""
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        raise StatusError("missing or unterminated frontmatter")

    fields = {}
    parent = None
    closed = False
    for line in lines[1:]:
        if line == "---":
            closed = True
            break
        if not line.strip():
            continue
        key, _, value = line.strip().partition(" ")
        key = key.rstrip(":")
        value = value.split(" #", 1)[0].strip()
        if line.startswith("  "):
            if parent is None:
                raise StatusError("nested field before top-level key")
            fields[parent][key] = value
            continue
        fields[key] = {} if not value else value
        parent = key

    if not closed:
        raise StatusError("missing or unterminated frontmatter")
    return fields


def read_status(path):
    text = Path(path).read_text()
    fields = parse_frontmatter(text)
    body = text.split("---", 2)[2]
    return fields, body


def next_action(body):
    """First non-heading line under `## Next action`, stopping at the next heading."""
    lines = body.splitlines()
    for i, line in enumerate(lines):
        if line.strip() == "## Next action":
            for following in lines[i + 1 :]:
                if following.startswith("#"):
                    break
                if following.strip():
                    return following.strip()
            break
    return ""


def validate(fields, body, tasks_path=None):
    errors = []

    phase = fields.get("phase", "")
    if phase not in PHASES:
        errors.append(f'unknown phase "{phase}"')

    approved = fields.get("approved", {})
    if phase in PHASES:
        for gate in GATES[: PHASES.index(phase)]:
            if approved.get(gate) not in ("true", "n/a"):
                errors.append(f"gate {gate} not approved at phase {phase}")

    action = next_action(body)
    if not action:
        errors.append("Next action is empty")

    if tasks_path:
        tasks = Path(tasks_path)
        if tasks.exists():
            for block in tasks.read_text().split("### ")[1:]:
                lines = [line.strip() for line in block.splitlines()]
                task_id = lines[0].split(" ")[0]
                if "Status: doing" in lines and not any(l.startswith("Note:") for l in lines):
                    errors.append(f"task {task_id} left doing without a note")

    return errors


def main(argv=None):
    parser = argparse.ArgumentParser(description="Inspect and validate fleet status")
    parser.add_argument("--check", action="store_true", help="validate only, exit 1 on any problem")
    parser.add_argument("--status", default="fleet/STATUS.md", help="path to the status file")
    args = parser.parse_args(argv)

    try:
        fields, body = read_status(args.status)
    except OSError:
        print("error: status file not found")
        return 1
    except StatusError as exc:
        print(f"error: {exc}")
        return 1

    errors = validate(fields, body, Path(args.status).parent / "TASKS.md")
    if args.check:
        if errors:
            for error in errors:
                print(f"error: {error}")
            return 1
        print("ok")
        return 0

    print(f"phase: {fields.get('phase', '')}")
    action = next_action(body)
    if action:
        print(f"next action: {action}")

    for error in errors:
        print(f"warning: {error}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
