# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Daily plan for Jordan's pets:

08:00 — Morning walk (30 min) for Biscuit [priority: high] — high priority owner asked for ~08:00.
09:00 — Feeding (10 min) for Biscuit [priority: high] — high priority, owner asked for ~09:00.
09:10 — Feeding (10 min) for Mochi [priority: high] — high priority, slotted in next available time.
09:20 — Litter cleanup (15 min) for Mochi [priority: medium] — medium priority, slotted in next available time.
09:35 — Enrichment play (20 min) for Biscuit [priority: low] — low priority, slotted in next available time.

Total scheduled: 85 min (5 tasks, 0 skipped)


## 🧪 Testing PawPal+

```bash
# Run the full test suite:
python -m pytest
========================= test session starts ==========================
platform win32 -- Python 3.11.9, pytest-9.0.3, pluggy-1.6.0
rootdir: C:\Users\shire\Documents\CodePathOrg\AI\ai110-module2show-pawpal-starter
plugins: anyio-4.11.0
collected 4 items                                                       

tests\test_pawpal.py ....                                         [100%]

========================== 4 passed in 0.11s ===========================

# Run with coverage:
pytest --cov

python -m pytest -v
========================= test session starts ==========================
platform win32 -- Python 3.11.9, pytest-9.0.3, pluggy-1.6.0 -- C:\Users\shire\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\shire\Documents\CodePathOrg\AI\ai110-module2show-pawpal-starter
plugins: anyio-4.11.0
collected 4 items                                                       

tests/test_pawpal.py::test_mark_complete_changes_status PASSED    [ 25%]
tests/test_pawpal.py::test_adding_task_increases_pet_task_count PASSED [ 50%]
tests/test_pawpal.py::test_scheduler_orders_high_priority_first PASSED [ 75%]
tests/test_pawpal.py::test_scheduler_skips_tasks_that_do_not_fit PASSED [100%]

========================== 4 passed in 0.04s ===========================

```

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | | e.g., by priority, duration |
| Filtering | | e.g., skip tasks if time runs out |
| Conflict handling | | e.g., overlapping time slots |
| Recurring tasks | | e.g., daily vs. weekly |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
