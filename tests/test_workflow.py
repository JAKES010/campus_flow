"""Engineer B: lifecycle, queue, reports."""
import unittest

from campusflow.reports import build_report, format_report
from campusflow.tickets import (
    TicketNotFoundError, ValidationError, WorkflowError, assign_ticket, create_ticket,
)
from campusflow.workflow import change_status, reopen_ticket, work_queue


def make(tickets, urgency="low", users=1):
    return create_ticket(tickets, "Issue", "Other", urgency, users)


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.tickets = []
        make(self.tickets)

    def test_unassigned_cannot_move_to_in_progress(self):
        with self.assertRaises(WorkflowError):
            change_status(self.tickets, "T001", "in_progress")
        self.assertEqual(self.tickets[0]["status"], "open")

    def test_assigned_ticket_progresses_to_resolved(self):
        assign_ticket(self.tickets, "T001", "Ada")
        change_status(self.tickets, "T001", "in_progress")
        self.assertEqual(self.tickets[0]["status"], "in_progress")
        change_status(self.tickets, "T001", "resolved")
        self.assertEqual(self.tickets[0]["status"], "resolved")

    def test_cannot_skip_open_to_resolved(self):
        assign_ticket(self.tickets, "T001", "Ada")
        with self.assertRaises(WorkflowError):
            change_status(self.tickets, "T001", "resolved")

    def test_resolved_only_modifiable_after_reopen(self):
        assign_ticket(self.tickets, "T001", "Ada")
        change_status(self.tickets, "T001", "in_progress")
        change_status(self.tickets, "T001", "resolved")
        with self.assertRaises(WorkflowError):
            change_status(self.tickets, "T001", "in_progress")
        with self.assertRaises(WorkflowError):
            assign_ticket(self.tickets, "T001", "Grace")
        reopen_ticket(self.tickets, "T001")
        self.assertEqual(self.tickets[0]["status"], "open")
        assign_ticket(self.tickets, "T001", "Grace")
        self.assertEqual(self.tickets[0]["assigned_to"], "Grace")

    def test_reopen_requires_resolved(self):
        with self.assertRaises(WorkflowError):
            reopen_ticket(self.tickets, "T001")

    def test_unknown_id_and_invalid_status(self):
        with self.assertRaises(TicketNotFoundError):
            change_status(self.tickets, "T404", "in_progress")
        with self.assertRaises(ValidationError):
            change_status(self.tickets, "T001", "done")


class QueueTests(unittest.TestCase):
    def test_sorted_by_priority_then_numeric_id(self):
        tickets = []
        make(tickets, "low", 1)        # T001 low
        make(tickets, "high", 12)      # T002 critical
        make(tickets, "medium", 1)     # T003 medium
        make(tickets, "high", 12)      # T004 critical
        make(tickets, "high", 1)       # T005 high
        order = [t["id"] for t in work_queue(tickets)]
        self.assertEqual(order, ["T002", "T004", "T005", "T003", "T001"])

    def test_numeric_not_text_id_order(self):
        tickets = [{"id": "T010", "priority": "low", "status": "open"},
                   {"id": "T002", "priority": "low", "status": "open"}]
        self.assertEqual([t["id"] for t in work_queue(tickets)], ["T002", "T010"])

    def test_queue_excludes_non_open(self):
        tickets = []
        make(tickets)
        make(tickets)
        tickets[0]["status"] = "resolved"
        self.assertEqual([t["id"] for t in work_queue(tickets)], ["T002"])

    def test_empty_queue(self):
        self.assertEqual(work_queue([]), [])


class ReportTests(unittest.TestCase):
    def test_empty_report(self):
        report = build_report([])
        self.assertEqual(report["total"], 0)
        self.assertTrue(all(v == 0 for v in report["by_status"].values()))
        self.assertTrue(all(v == 0 for v in report["by_priority"].values()))
        self.assertIn("Total tickets: 0", format_report(report))

    def test_report_counts(self):
        tickets = []
        make(tickets, "high", 12)
        make(tickets, "low", 1)
        make(tickets, "low", 1)
        tickets[2]["status"] = "resolved"
        report = build_report(tickets)
        self.assertEqual(report["total"], 3)
        self.assertEqual(report["by_status"], {"open": 2, "in_progress": 0, "resolved": 1})
        self.assertEqual(report["by_priority"],
                         {"critical": 1, "high": 0, "medium": 0, "low": 2})


if __name__ == "__main__":
    unittest.main()
