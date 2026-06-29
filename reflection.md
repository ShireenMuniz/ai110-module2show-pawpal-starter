# PawPal+ Project Reflection

## 1. System Design

**Core user actions**
1. Add a pet — the owner registers a pet with a name and species.
2. Add a care task — attach an activity (duration, priority, optional preferred time) to a pet.
3. Generate today's schedule — produce an ordered daily plan that fits tasks into the available time by priority, and explain the choices.


**a. Initial design**
- I chose four classes. Task is a dataclass holding one activity's details (duration,priority, frequency, preferred time, completion). Pet is a dataclass that owns a list of Tasks. Owner manages a list of Pets and can flatten every task across pets. Scheduler is the "brain": it reads the owner's tasks and produces an ordered DailyPlan, sorting by priority and packing tasks into an available-time budget.


**b. Design changes**
- Yes. My skeleton had Scheduler return a raw list, but during implementation I added two helper dataclasses ScheduledItem (a task + start time + reason) and DailyPlan (scheduled items + skipped tasks). This made the output easy to explain and let me track skipped tasks separately. I also added a preferred_time tie-breaker so fixed-time tasks (like feeding at
09:00) land in their slot instead of being packed purely by priority.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**
- The scheduler considers three constraints: total time available for the day, each task's priority (high/medium/low), and the owner's optional preferred start time for a task. Priority matters most high-priority care (walks, feeding, meds) should never be dropped before low-priority enrichment. Time available is the hard limit that decides how many tasks fit, and preferred_time is a soft preference used as a tie-breaker so fixed-time tasks land in their slot.

**b. Tradeoffs**
- My conflict detector only flags tasks that share the exact same preferred_time (e.g. two tasks both at "08:00"). It does not detect overlapping durations, a 30-min task at 08:00 and another at 08:15 won't be flagged even though they collide. I chose exact-match because it is simple, fast, and returns a clear warning string without crashing; full overlap detection would need start+end interval math for every pair of tasks. For a personal pet-care planner, exact-time clashes are the common and important case.

---

## 3. AI Collaboration

**a. How you used AI**
- I used my AI assistant for design brainstorming (turning the scenario into four classes),generating the Mermaid UML, scaffolding the dataclasses, and drafting tests. The most helpful prompts were specific and file-attached e.g. "based on my skeletons, how should the Scheduler get tasks from the Owner's pets?" rather than vague "build me an app."


**b. Judgment and verification**
- The assistant first had the Scheduler reach directly into Pet.tasks. I rejected that and kept a single accessor (Owner.get_tasks_with_pets) so the Scheduler never depends on Pet's internals. I verified suggestions by running main.py and the pytest suite — for example, a recurrence edit only "counted" once test_completing_daily_task_creates_next_day_occurrence passed with the correct next date.

**c. AI strategy**
- Inline editing was best for boilerplate (dataclasses, tests); chat was best for design questions. Keeping separate chat sessions per phase stopped earlier context from polluting later prompts (e.g. testing discussion didn't drag in UI code). Overall I treated the AI as a fast junior engineer whose work I reviewed, not as the decision-maker.


---

## 4. Testing and Verification

**a. What you tested**
- I tested completion flips, task counting, priority ordering, time-budget skipping, chronological sorting, daily/weekly recurrence dates, conflict detection, filtering and the empty-pet edge case. These cover the core "brain" decisions a user relies on.


**b. Confidence**
- I'm fairly confident (4/5), 12 tests pass. Next I'd test overlapping-duration conflicts and multi-day recurrence streaks.

---

## 5. Reflection

**a. What went well**
- I'm most satisfied with the explainable scheduler every item carries a reason.


**b. What you would improve**
- I'd replace exact-time conflict checks with interval-overlap detection and add JSON persistence so data survives restarts.


**c. Key takeaway**
- Biggest takeaway: I'm the lead architect. AI accelerates drafting, but I decide the class boundaries, reject designs that leak internals and verify everything with tests.


## 5. Smarter Scheduling

**b. Tradeoffs**
- My conflict detector only flags tasks that share the exact same preferred_time (e.g. two tasks both at "08:00"). It does not detect *overlapping durations* — a 30-min task at 08:00 and another at 08:15 won't be flagged even though they collide.I chose exact-match because it's simple, fast, and returns a clear warning without crashing; full overlap detection would need start+end interval math for every pair.For a personal  pet-care planner, exact-time clashes are the common, important case.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Sorts by preferred_time ("HH:MM"); untimed tasks go last |
| Filtering | `Scheduler.filter_tasks()` | Filter by pet name and/or completion status |
| Conflict handling | `Scheduler.detect_conflicts()` | Warns on tasks sharing the same preferred_time |
| Recurring tasks | `Task.next_occurrence()`, `Pet.complete_task()` | Completing a daily/weekly task creates the next occurrence via timedelta |


