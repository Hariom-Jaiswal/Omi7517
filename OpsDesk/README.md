# OpsDesk - OpenEnv

## Motivation
Simulate a real-world business operations workflow for training agentic AI models on email parsing, task extraction, and calendar scheduling under varying difficulty constraints.

## Environment Description
**OpsDesk** provides an environment where AI agents process incoming emails, classify them, extract actionable tasks, schedule meetings, and respond. It meets the constraints of running well under 2 vCPU and 8GB RAM, featuring purely deterministic graders without randomness in scoring.

## Action & Observation Space
* **Observation**: Inbox (emails with IDs, subject, body), Tasks, Calendar.
* **Actions**: `classify_email`, `extract_task`, `schedule_meeting`, `reply_email`, `ignore_email`. Each requires `email_id` and optional `metadata`.

## Tasks
1. **EASY**: Classify emails correctly.
2. **MEDIUM**: Extract tasks and schedule meetings.
3. **HARD**: Handle multiple conflicting emails with limited time slots.

## Reward Function
Dense rewards are provided during steps:
* +0.2 for correct classification
* +0.3 for correct task extraction
* +0.3 for correct scheduling
* -0.2 for incorrect actions
* -0.1 for repeated actions

## Setup
1. `pip install -r requirements.txt`
2. `uvicorn app:app --host 0.0.0.0 --port 7860`

## Inference
Run `python inference.py`. Configure using environmental variables:
`OPENAI_API_KEY`, `API_BASE_URL`, `MODEL_NAME`, `HF_TOKEN`.

## Baseline Score
A correct sequence on the HARD task yields a score of 1.0 (with complete classification accuracy, correct scheduling, and task extraction).
