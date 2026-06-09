"""Rank tasks using a simple impact/urgency/effort score."""

from __future__ import annotations

import json
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


def task_to_mapping(task: Task) -> dict[str, Any]:
    return {
        "name": task.name,
        "impact": task.impact,
        "urgency": task.urgency,
        "effort": task.effort,
        "score": round(task.score, 2),
    }


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) != 1:
        print("Usage: python -m src.task_ranker '[{\"name\":\"Task\"}]'", file=sys.stderr)
        return 2
    rows = json.loads(args[0])
    tasks = [task_from_mapping(row) for row in rows]
    print(json.dumps([task_to_mapping(task) for task in rank_tasks(tasks)], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
