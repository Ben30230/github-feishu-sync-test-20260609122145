# GitHub Feishu Sync Test

GitHub Feishu Sync Test is a small Python CLI project used to exercise realistic GitHub to Feishu update broadcasts.

The first module, `task_ranker`, ranks project tasks with a transparent impact/urgency/effort score. It is intentionally lightweight so every sync test commit reads like a normal open source project change.

## Usage

```bash
python3 -m src.task_ranker '[{"name":"Fix sync failure","impact":5,"urgency":5,"effort":3}]'
```

## Test

```bash
python3 -m unittest discover -s tests
```
