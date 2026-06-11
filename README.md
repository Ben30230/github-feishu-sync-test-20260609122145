# GitHub Feishu Sync Test

GitHub Feishu Sync Test is a small Python CLI project used to exercise realistic GitHub to Feishu update broadcasts.

The first module, `task_ranker`, ranks project tasks with a transparent impact/urgency/effort score. It is intentionally lightweight so every sync test commit reads like a normal open source project change.

Task Ranker can also select a plan that fits an effort budget. It ranks tasks
first, then keeps the highest-value items that fit within the remaining budget.

## Usage

```bash
python3 -m src.task_ranker '[{"name":"Fix sync failure","impact":5,"urgency":5,"effort":3}]'
```

```bash
python3 -m src.task_ranker '[{"name":"Fix webhook retry","impact":4,"urgency":5,"effort":3}]' --budget 5
```

## Test

```bash
python3 -m unittest discover -s tests
```
