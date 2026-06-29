"""Tests for core PawPal+ behaviors."""

from pawpal_system import Owner, Pet, Task, Scheduler


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
