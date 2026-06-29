# PawPal+ Project Reflection

## 1. System Design

**Core user actions**

1. Add a pet — the owner registers a pet with a name and species.
2. Add a care task — attach an activity (duration, priority, optional preferred time) to a pet.
3. Generate today's schedule — produce an ordered daily plan that fits tasks into the available time by priority, and explain the choices.


**a. Initial design**
I chose four classes. Task is a dataclass holding one activity's details (duration,priority, frequency, preferred time, completion). Pet is a dataclass that owns a list of Tasks. Owner manages a list of Pets and can flatten every task across pets. Scheduler is the "brain": it reads the owner's tasks and produces an ordered DailyPlan, sorting by priority and packing tasks into an available-time budget.


**b. Design changes**
Yes. My skeleton had Scheduler return a raw list, but during implementation I added two helper dataclasses — ScheduledItem (a task + start time + reason) and DailyPlan (scheduled items + skipped tasks). This made the output easy to explain and let me track skipped tasks separately. I also added a preferred_time tie-breaker so fixed-time tasks (like feeding at
09:00) land in their slot instead of being packed purely by priority.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler considers three constraints: total time available for the day, each
task's priority (high/medium/low), and the owner's optional preferred start time for a
task. Priority matters most — high-priority care (walks, feeding, meds) should never be
dropped before low-priority enrichment. Time available is the hard limit that decides
how many tasks fit, and preferred_time is a soft preference used as a tie-breaker so
fixed-time tasks land in their slot.

**b. Tradeoffs**

My conflict detector only flags tasks that share the exact same preferred_time (e.g.
two tasks both at "08:00"). It does not detect overlapping durations — a 30-min task at
08:00 and another at 08:15 won't be flagged even though they collide. I chose exact-match
because it is simple, fast, and returns a clear warning string without crashing; full
overlap detection would need start+end interval math for every pair of tasks. For a
personal pet-care planner, exact-time clashes are the common and important case.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

## 5. Smarter Scheduling

**b. Tradeoffs**
My conflict detector only flags tasks that share the exact same preferred_time (e.g. two tasks both at "08:00"). It does not detect *overlapping durations* — a 30-min task at 08:00 and another at 08:15 won't be flagged even though they collide.I chose exact-match because it's simple, fast, and returns a clear warning without crashing; full overlap detection would need start+end interval math for every pair.For a personal  pet-care planner, exact-time clashes are the common, important case.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Sorts by preferred_time ("HH:MM"); untimed tasks go last |
| Filtering | `Scheduler.filter_tasks()` | Filter by pet name and/or completion status |
| Conflict handling | `Scheduler.detect_conflicts()` | Warns on tasks sharing the same preferred_time |
| Recurring tasks | `Task.next_occurrence()`, `Pet.complete_task()` | Completing a daily/weekly task creates the next occurrence via timedelta |


