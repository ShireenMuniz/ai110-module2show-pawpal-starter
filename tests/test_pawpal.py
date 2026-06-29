"""Tests for core PawPal+ behaviors."""

from pawpal_system import Owner, Pet, Task, Scheduler
from datetime import date, timedelta


def test_mark_complete_changes_status():
    """mark_complete() should flip a task's completed flag to True."""
    task = Task("Walk", 30, priority="high")
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_adding_task_increases_pet_task_count():
    """Adding a task to a pet should grow its task count by one."""
    pet = Pet(name="Biscuit")
    assert pet.task_count() == 0
    pet.add_task(Task("Feeding", 10))
    assert pet.task_count() == 1


def test_scheduler_orders_high_priority_first():
    """High-priority tasks should appear before low-priority ones in the plan."""
    owner = Owner("Jordan")
    pet = owner.add_pet(Pet("Mochi"))
    pet.add_task(Task("Play", 20, priority="low"))
    pet.add_task(Task("Walk", 20, priority="high"))
    plan = Scheduler().build_daily_plan(owner)
    assert plan.items[0].task.title == "Walk"


def test_scheduler_skips_tasks_that_do_not_fit():
    """Tasks exceeding the time budget should be skipped, not scheduled."""
    owner = Owner("Jordan")
    pet = owner.add_pet(Pet("Mochi"))
    pet.add_task(Task("Long walk", 60, priority="high"))
    pet.add_task(Task("Extra walk", 60, priority="low"))
    plan = Scheduler(available_minutes=60).build_daily_plan(owner)
    assert len(plan.items) == 1
    assert len(plan.skipped) == 1


def test_sort_by_time_orders_chronologically():
    """sort_by_time should return tasks in ascending HH:MM order."""
    tasks = [
        Task("Evening", 20, preferred_time="18:00"),
        Task("Morning", 20, preferred_time="08:00"),
        Task("Noon", 20, preferred_time="12:00"),
    ]
    ordered = [t.title for t in Scheduler.sort_by_time(tasks)]
    assert ordered == ["Morning", "Noon", "Evening"]


def test_untimed_tasks_sort_last():
    """Tasks without a preferred_time should appear after timed ones."""
    tasks = [Task("NoTime", 20), Task("Morning", 20, preferred_time="08:00")]
    ordered = [t.title for t in Scheduler.sort_by_time(tasks)]
    assert ordered == ["Morning", "NoTime"]


def test_completing_daily_task_creates_next_day_occurrence():
    """Completing a daily task adds a new task due one day later."""
    pet = Pet("Biscuit")
    task = pet.add_task(Task("Walk", 30, frequency="daily", due_date=date(2026, 1, 1)))
    new_task = pet.complete_task(task)
    assert task.completed is True
    assert pet.task_count() == 2
    assert new_task.due_date == date(2026, 1, 2)
    assert new_task.completed is False


def test_completing_weekly_task_advances_one_week():
    """A weekly task's next occurrence is 7 days later."""
    pet = Pet("Mochi")
    task = pet.add_task(Task("Bath", 20, frequency="weekly", due_date=date(2026, 1, 1)))
    new_task = pet.complete_task(task)
    assert new_task.due_date == date(2026, 1, 1) + timedelta(weeks=1)


def test_detect_conflicts_flags_same_time():
    """Two tasks at the same preferred_time should produce one warning."""
    owner = Owner("Jordan")
    pet = owner.add_pet(Pet("Biscuit"))
    pet.add_task(Task("Walk", 30, preferred_time="08:00"))
    pet.add_task(Task("Feed", 10, preferred_time="08:00"))
    warnings = Scheduler.detect_conflicts(owner)
    assert len(warnings) == 1
    assert "08:00" in warnings[0]


def test_no_conflict_when_times_differ():
    """Distinct preferred times should produce no warnings."""
    owner = Owner("Jordan")
    pet = owner.add_pet(Pet("Biscuit"))
    pet.add_task(Task("Walk", 30, preferred_time="08:00"))
    pet.add_task(Task("Feed", 10, preferred_time="09:00"))
    assert Scheduler.detect_conflicts(owner) == []


def test_filter_tasks_by_pet_name():
    """filter_tasks should return only the named pet's tasks."""
    owner = Owner("Jordan")
    a = owner.add_pet(Pet("Biscuit"))
    b = owner.add_pet(Pet("Mochi"))
    a.add_task(Task("Walk", 30))
    b.add_task(Task("Feed", 10))
    titles = [t.title for t in Scheduler.filter_tasks(owner, pet_name="Biscuit")]
    assert titles == ["Walk"]


def test_pet_with_no_tasks_produces_empty_plan():
    """A pet with no tasks should yield an empty plan, not an error (edge case)."""
    owner = Owner("Jordan")
    owner.add_pet(Pet("Biscuit"))
    plan = Scheduler().build_daily_plan(owner)
    assert plan.items == []
    assert plan.skipped == []

