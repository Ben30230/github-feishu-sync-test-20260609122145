import json
import subprocess
import sys
import unittest

from src.task_ranker import Task, rank_tasks, task_from_mapping


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


if __name__ == "__main__":
    unittest.main()
