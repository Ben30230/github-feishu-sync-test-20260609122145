"""Rank tasks using a simple impact/urgency/effort score."""

from __future__ import annotations

import json
import argparse
import sys
from dataclasses import dataclass
from typing import Any, Iterable


@dataclass(frozen=True)
class Task:
    name: str
    impact: int = 1
    urgency: int = 1
    effort: int = 1

    @property
    def score(self) -> float:
        return self.impact * 3 + self.urgency * 2 - self.effort


def task_from_mapping(data: dict[str, Any]) -> Task:
    return Task(
        name=str(data["name"]),
        impact=int(data.get("impact", 1)),
        urgency=int(data.get("urgency", 1)),
        effort=int(data.get("effort", 1)),
    )


def rank_tasks(tasks: Iterable[Task]) -> list[Task]:
    return sorted(tasks, key=lambda item: (-item.score, item.name.lower()))


def select_plan(tasks: Iterable[Task], max_effort: int) -> list[Task]:
    plan: list[Task] = []
    remaining = max_effort
    for task in rank_tasks(tasks):
        if task.effort <= remaining:
            plan.append(task)
            remaining -= task.effort
    return plan


def plan_summary(tasks: Iterable[Task], max_effort: int) -> dict[str, Any]:
    plan = select_plan(tasks, max_effort)
    used_effort = sum(task.effort for task in plan)
    return {
        "selected": [task.name for task in plan],
        "used_effort": used_effort,
        "remaining_effort": max_effort - used_effort,
    }


def task_to_mapping(task: Task) -> dict[str, Any]:
    return {
        "name": task.name,
        "impact": task.impact,
        "urgency": task.urgency,
        "effort": task.effort,
        "score": round(task.score, 2),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Rank tasks by impact, urgency, and effort.")
    parser.add_argument("tasks_json", help="JSON array of task objects.")
    parser.add_argument("--budget", type=int, help="Select the best ranked tasks within this effort budget.")
    args = parser.parse_args(sys.argv[1:] if argv is None else argv)

    rows = json.loads(args.tasks_json)
    tasks = [task_from_mapping(row) for row in rows]
    selected = select_plan(tasks, args.budget) if args.budget is not None else rank_tasks(tasks)
    print(json.dumps([task_to_mapping(task) for task in selected], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
