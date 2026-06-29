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

Output from running `python main.py`:

```
Daily plan for Jordan's pets:

08:00 — Feeding (10 min) for Mochi [priority: high] — high priority, owner asked for ~08:00.
08:10 — Morning walk (30 min) for Biscuit [priority: high] — high priority, owner asked for ~08:00.
18:00 — Evening walk (30 min) for Biscuit [priority: high] — high priority, owner asked for ~18:00.
18:30 — Litter cleanup (15 min) for Mochi [priority: medium] — medium priority, slotted in next available time.
18:45 — Enrichment play (20 min) for Biscuit [priority: low] — low priority, slotted in next available time.

--- Tasks sorted by time ---
  08:00  Morning walk
  08:00  Feeding
  18:00  Evening walk
  --:--  Enrichment play
  --:--  Litter cleanup

--- High-detail filters ---
Biscuit's tasks: ['Evening walk', 'Morning walk', 'Enrichment play']

--- Conflicts ---
Conflict at 08:00: Morning walk (Biscuit), Feeding (Mochi)

--- Recurring task demo ---
Completed 'Morning walk'. Tasks went 3 -> 4. Next due: 2026-06-30
```


## 🧪 Testing PawPal+

Run the full test suite with:

```bash
python -m pytest
```

The suite covers task completion, task counting, schedule ordering by priority,
time-budget skipping, chronological sorting, untimed-task ordering, daily/weekly
recurrence, conflict detection, filtering by pet, and the empty-pet edge case.

```
============================= test session starts =============================
platform win32 -- Python 3.11.9, pytest-9.0.3, pluggy-1.6.0
rootdir: C:\Users\shire\Documents\CodePathOrg\AI\ai110-module2show-pawpal-starter
plugins: anyio-4.11.0
collected 12 items

tests/test_pawpal.py::test_mark_complete_changes_status PASSED           [  8%]
tests/test_pawpal.py::test_adding_task_increases_pet_task_count PASSED   [ 16%]
tests/test_pawpal.py::test_scheduler_orders_high_priority_first PASSED   [ 25%]
tests/test_pawpal.py::test_scheduler_skips_tasks_that_do_not_fit PASSED  [ 33%]
tests/test_pawpal.py::test_sort_by_time_orders_chronologically PASSED    [ 41%]
tests/test_pawpal.py::test_untimed_tasks_sort_last PASSED                [ 50%]
tests/test_pawpal.py::test_completing_daily_task_creates_next_day_occurrence PASSED [ 58%]
tests/test_pawpal.py::test_completing_weekly_task_advances_one_week PASSED [ 66%]
tests/test_pawpal.py::test_detect_conflicts_flags_same_time PASSED       [ 75%]
tests/test_pawpal.py::test_no_conflict_when_times_differ PASSED          [ 83%]
tests/test_pawpal.py::test_filter_tasks_by_pet_name PASSED               [ 91%]
tests/test_pawpal.py::test_pet_with_no_tasks_produces_empty_plan PASSED  [100%]

============================= 12 passed in 0.04s ==============================
```

**Confidence level:** ⭐⭐⭐⭐☆ (4/5) — core scheduling, recurrence, and conflict
logic are well covered. Next I'd add tests for overlapping-duration conflicts and
multi-day recurrence streaks.

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Sorts by `preferred_time` ("HH:MM"); untimed tasks go last |
| Filtering | `Scheduler.filter_tasks()` | Filter by pet name and/or completion status |
| Conflict handling | `Scheduler.detect_conflicts()` | Warns on tasks sharing the same `preferred_time` (exact match) |
| Recurring tasks | `Task.next_occurrence()`, `Pet.complete_task()` | Completing a daily/weekly task creates the next occurrence via `timedelta` |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
