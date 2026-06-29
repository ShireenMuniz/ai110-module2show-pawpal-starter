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

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

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
