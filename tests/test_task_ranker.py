import json
import subprocess
import sys
import unittest

from src.task_ranker import Task, plan_summary, rank_tasks, select_plan, task_from_mapping


class TaskRankerTests(unittest.TestCase):
    def test_ranks_tasks_by_impact_urgency_and_effort(self):
        tasks = [
            Task(name="Polish docs", impact=4, urgency=2, effort=1),
            Task(name="Fix sync failure", impact=5, urgency=5, effort=3),
            Task(name="Refactor helper", impact=3, urgency=1, effort=2),
        ]

        ranked = rank_tasks(tasks)

        self.assertEqual([item.name for item in ranked], ["Fix sync failure", "Polish docs", "Refactor helper"])
        self.assertGreater(ranked[0].score, ranked[1].score)

    def test_builds_task_from_mapping_with_defaults(self):
        task = task_from_mapping({"name": "Review release notes", "impact": 3})

        self.assertEqual(task.name, "Review release notes")
        self.assertEqual(task.impact, 3)
        self.assertEqual(task.urgency, 1)
        self.assertEqual(task.effort, 1)

    def test_select_plan_respects_effort_budget_after_ranking(self):
        tasks = [
            Task(name="Large launch", impact=5, urgency=5, effort=8),
            Task(name="Fix webhook retry", impact=4, urgency=5, effort=3),
            Task(name="Polish docs", impact=3, urgency=2, effort=2),
        ]

        plan = select_plan(tasks, max_effort=5)

        self.assertEqual([item.name for item in plan], ["Fix webhook retry", "Polish docs"])
        self.assertLessEqual(sum(item.effort for item in plan), 5)

    def test_plan_summary_reports_selected_effort_and_remaining_budget(self):
        tasks = [
            Task(name="Large launch", impact=5, urgency=5, effort=8),
            Task(name="Fix webhook retry", impact=4, urgency=5, effort=3),
            Task(name="Polish docs", impact=3, urgency=2, effort=2),
        ]

        summary = plan_summary(tasks, max_effort=6)

        self.assertEqual(summary["selected"], ["Fix webhook retry", "Polish docs"])
        self.assertEqual(summary["used_effort"], 5)
        self.assertEqual(summary["remaining_effort"], 1)


class TaskRankerCliTests(unittest.TestCase):
    def test_cli_outputs_ranked_json(self):
        payload = json.dumps(
            [
                {"name": "Small cleanup", "impact": 2, "urgency": 1, "effort": 1},
                {"name": "Ship sync status", "impact": 5, "urgency": 4, "effort": 2},
            ]
        )

        result = subprocess.run(
            [sys.executable, "-m", "src.task_ranker", payload],
            check=True,
            capture_output=True,
            text=True,
        )

        ranked = json.loads(result.stdout)
        self.assertEqual(ranked[0]["name"], "Ship sync status")
        self.assertIn("score", ranked[0])

    def test_cli_budget_outputs_selected_plan(self):
        payload = json.dumps(
            [
                {"name": "Large launch", "impact": 5, "urgency": 5, "effort": 8},
                {"name": "Fix webhook retry", "impact": 4, "urgency": 5, "effort": 3},
                {"name": "Polish docs", "impact": 3, "urgency": 2, "effort": 2},
            ]
        )

        result = subprocess.run(
            [sys.executable, "-m", "src.task_ranker", payload, "--budget", "5"],
            check=True,
            capture_output=True,
            text=True,
        )

        ranked = json.loads(result.stdout)
        self.assertEqual([item["name"] for item in ranked], ["Fix webhook retry", "Polish docs"])


if __name__ == "__main__":
    unittest.main()
