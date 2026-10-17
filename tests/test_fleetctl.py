import tempfile
import unittest
from pathlib import Path

import fleetctl


VALID = """---
phase: developer
pilot: fleetctl
owner: orchestrator
approved:
  plan: true
  design: true
  architecture: true
---

# Fleet status

## Next action

implement TASK-003

## Log

- (empty)
"""


def write(tmp, content, name="STATUS.md"):
    path = Path(tmp) / name
    path.write_text(content)
    return path


class FleetctlTest(unittest.TestCase):
    def test_valid_status(self):
        with tempfile.TemporaryDirectory() as tmp:
            fields, body = fleetctl.read_status(write(tmp, VALID))
            self.assertEqual(fields["phase"], "developer")
            self.assertEqual(fields["approved"]["plan"], "true")
            self.assertEqual(fleetctl.validate(fields, body), [])

    def test_unknown_phase(self):
        with tempfile.TemporaryDirectory() as tmp:
            fields, body = fleetctl.read_status(write(tmp, VALID.replace("phase: developer", "phase: review")))
            self.assertIn('unknown phase "review"', fleetctl.validate(fields, body))

    def test_unapproved_gate_at_later_phase(self):
        with tempfile.TemporaryDirectory() as tmp:
            fields, body = fleetctl.read_status(write(tmp, VALID.replace("  plan: true", "  plan: false")))
            self.assertIn("gate plan not approved at phase developer", fleetctl.validate(fields, body))

    def test_gate_marked_na_is_valid(self):
        with tempfile.TemporaryDirectory() as tmp:
            fields, body = fleetctl.read_status(write(tmp, VALID.replace("  design: true", "  design: n/a")))
            self.assertEqual(fleetctl.validate(fields, body), [])

    def test_empty_next_action(self):
        with tempfile.TemporaryDirectory() as tmp:
            fields, body = fleetctl.read_status(write(tmp, VALID.replace("implement TASK-003", "")))
            self.assertIn("Next action is empty", fleetctl.validate(fields, body))

    def test_task_left_doing_without_note(self):
        with tempfile.TemporaryDirectory() as tmp:
            tasks = write(tmp, "### TASK-003 — CLI\nStatus: doing\n", "TASKS.md")
            fields, body = fleetctl.read_status(write(tmp, VALID))
            self.assertIn("task TASK-003 left doing without a note", fleetctl.validate(fields, body, tasks))

    def test_task_left_doing_with_note_is_valid(self):
        with tempfile.TemporaryDirectory() as tmp:
            tasks = write(tmp, "### TASK-003 — CLI\nStatus: doing\nNote: argparse wired, --check pending\n", "TASKS.md")
            fields, body = fleetctl.read_status(write(tmp, VALID))
            self.assertEqual(fleetctl.validate(fields, body, tasks), [])

    def test_unterminated_frontmatter(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(fleetctl.StatusError):
                fleetctl.read_status(write(tmp, "---\nphase: plan\n\n# Status\n"))

    def test_check_exit_codes(self):
        with tempfile.TemporaryDirectory() as tmp:
            status = write(tmp, VALID)
            self.assertEqual(fleetctl.main(["--check", "--status", str(status)]), 0)
            bad = write(tmp, VALID.replace("phase: developer", "phase: review"))
            self.assertEqual(fleetctl.main(["--check", "--status", str(bad)]), 1)

    def test_missing_status_file(self):
        self.assertEqual(fleetctl.main(["--check", "--status", "/nonexistent/STATUS.md"]), 1)


if __name__ == "__main__":
    unittest.main()
