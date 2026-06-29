"""PawPal+ logic layer: backend classes for owners, pets, tasks, and scheduling.

UI-agnostic so it can be driven from a CLI demo (main.py), tests, or Streamlit (app.py).
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional

# Priority -> sort weight (lower = scheduled earlier / preferred).
PRIORITY_WEIGHT = {"high": 0, "medium": 1, "low": 2}


@dataclass
class Task:
    """A single pet-care activity (walk, feeding, meds, etc.)."""
    title: str
    duration_minutes: int
    priority: str = "medium"
    frequency: str = "daily"            # "daily" or "weekly"
    preferred_time: Optional[str] = None  # "HH:MM" for a fixed slot
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark this task as done for the day."""
        self.completed = True

    def reset(self) -> None:
        """Clear completion status (e.g. at the start of a new day)."""
        self.completed = False

    def priority_weight(self) -> int:
        """Numeric sort weight for this task's priority (unknown -> medium)."""
        return PRIORITY_WEIGHT.get(self.priority, PRIORITY_WEIGHT["medium"])


@dataclass
class Pet:
    """A pet that owns its own list of care tasks."""
    name: str
    species: str = "dog"
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> Task:
        """Attach a task to this pet and return it."""
        self.tasks.append(task)
        return task

    def task_count(self) -> int:
        """How many tasks this pet currently has."""
        return len(self.tasks)


@dataclass
class Owner:
    """The human user: holds basic info and manages one or more pets."""
    name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> Pet:
        """Register a pet with this owner and return it."""
        self.pets.append(pet)
        return pet

    def get_all_tasks(self) -> List[Task]:
        """Every task across all of this owner's pets (flattened)."""
        return [task for pet in self.pets for task in pet.tasks]

    def get_tasks_with_pets(self) -> List[tuple]:
        """(pet, task) pairs so callers know which pet each task belongs to."""
        return [(pet, task) for pet in self.pets for task in pet.tasks]


@dataclass
class ScheduledItem:
    """One entry in a plan: a task placed at a start time, with reasoning."""
    start_time: str  # "HH:MM"
    pet: Pet
    task: Task
    reason: str


@dataclass
class DailyPlan:
    """Result of scheduling: ordered items plus tasks that didn't fit."""
    items: List[ScheduledItem] = field(default_factory=list)
    skipped: List[tuple] = field(default_factory=list)  # (pet, task, reason)

    def total_minutes(self) -> int:
        """Total scheduled time across all placed tasks."""
        return sum(item.task.duration_minutes for item in self.items)


class Scheduler:
    """The 'brain': turns an owner's pets/tasks into an ordered daily plan.

    Rules, in order of importance:
      1. Priority first (high > medium > low).
      2. Within a priority, an explicit preferred_time wins, then shorter tasks.
      3. Pack tasks into the available-time budget; skip what no longer fits.
    """

    def __init__(self, start_time: str = "08:00", available_minutes: int = 480):
        """Set the day's start time and total available minutes."""
        self.start_minute = self._to_minutes(start_time)
        self.available_minutes = available_minutes

    @staticmethod
    def _to_minutes(hhmm: str) -> int:
        """Convert 'HH:MM' to minutes past midnight."""
        h, m = hhmm.split(":")
        return int(h) * 60 + int(m)

    @staticmethod
    def _to_hhmm(total_minutes: int) -> str:
        """Convert minutes past midnight back to 'HH:MM'."""
        return f"{(total_minutes // 60) % 24:02d}:{total_minutes % 60:02d}"

    def _sort_key(self, pet_task: tuple):
        """Sort by priority, then preferred-time presence/value, then duration."""
        _, task = pet_task
        has_preferred = 0 if task.preferred_time else 1
        preferred = self._to_minutes(task.preferred_time) if task.preferred_time else 0
        return (task.priority_weight(), has_preferred, preferred, task.duration_minutes)

    def build_daily_plan(self, owner: Owner) -> DailyPlan:
        """Generate an ordered DailyPlan for the owner within the time budget."""
        plan = DailyPlan()
        ordered = sorted(owner.get_tasks_with_pets(), key=self._sort_key)

        current = self.start_minute
        used = 0
        for pet, task in ordered:
            if used + task.duration_minutes > self.available_minutes:
                reason = (f"Not enough time left ({self.available_minutes - used} min free, "
                          f"needs {task.duration_minutes} min).")
                plan.skipped.append((pet, task, reason))
                continue

            if task.preferred_time:
                start = max(current, self._to_minutes(task.preferred_time))
                reason = f"{task.priority} priority, owner asked for ~{task.preferred_time}."
            else:
                start = current
                reason = f"{task.priority} priority, slotted in next available time."

            plan.items.append(ScheduledItem(self._to_hhmm(start), pet, task, reason))
            current = start + task.duration_minutes
            used += task.duration_minutes

        return plan

    def explain_plan(self, plan: DailyPlan) -> str:
        """Human-readable, line-by-line explanation of a plan."""
        lines = []
        for item in plan.items:
            lines.append(
                f"{item.start_time} — {item.task.title} ({item.task.duration_minutes} min) "
                f"for {item.pet.name} [priority: {item.task.priority}] — {item.reason}"
            )
        for pet, task, reason in plan.skipped:
            lines.append(f"SKIPPED — {task.title} for {pet.name}: {reason}")
        return "\n".join(lines) if lines else "No tasks to schedule."
