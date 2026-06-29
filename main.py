"""CLI demo for PawPal+: builds a sample owner/pets/tasks and prints today's schedule."""

from pawpal_system import Owner, Pet, Task, Scheduler


def main() -> None:
    owner = Owner(name="Jordan")
    biscuit = owner.add_pet(Pet(name="Biscuit", species="dog"))
    mochi = owner.add_pet(Pet(name="Mochi", species="cat"))

    # Added intentionally out of chronological order.
    biscuit.add_task(Task("Evening walk", 30, priority="high", preferred_time="18:00"))
    biscuit.add_task(Task("Morning walk", 30, priority="high", preferred_time="08:00"))
    biscuit.add_task(Task("Enrichment play", 20, priority="low"))
    mochi.add_task(Task("Feeding", 10, priority="high", preferred_time="08:00"))  # conflict @ 08:00
    mochi.add_task(Task("Litter cleanup", 15, priority="medium"))

    scheduler = Scheduler(start_time="08:00", available_minutes=480)

    print(f"Daily plan for {owner.name}'s pets:\n")
    print(scheduler.explain_plan(scheduler.build_daily_plan(owner)))

    print("\n--- Tasks sorted by time ---")
    for t in scheduler.sort_by_time(owner.get_all_tasks()):
        print(f"  {t.preferred_time or '--:--'}  {t.title}")

    print("\n--- High-detail filters ---")
    print("Biscuit's tasks:", [t.title for t in scheduler.filter_tasks(owner, pet_name="Biscuit")])

    print("\n--- Conflicts ---")
    conflicts = scheduler.detect_conflicts(owner)
    print("\n".join(conflicts) if conflicts else "No conflicts.")

    print("\n--- Recurring task demo ---")
    walk = biscuit.tasks[1]  # Morning walk (daily)
    before = biscuit.task_count()
    new_task = biscuit.complete_task(walk)
    print(f"Completed '{walk.title}'. Tasks went {before} -> {biscuit.task_count()}. "
          f"Next due: {new_task.due_date}")


if __name__ == "__main__":
    main()
