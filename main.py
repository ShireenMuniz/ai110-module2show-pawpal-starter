"""CLI demo for PawPal+: builds a sample owner/pets/tasks and prints today's schedule."""

from pawpal_system import Owner, Pet, Task, Scheduler
from tabulate import tabulate

# Emoji for a task based on a keyword in its title.
TASK_EMOJI = {
    "walk": "🐕", "feed": "🍽️", "med": "💊", "groom": "🛁",
    "play": "🎾", "enrich": "🧩", "litter": "🧹",
}
# Color dot per priority level.
PRIORITY_EMOJI = {"high": "🔴", "medium": "🟡", "low": "🟢"}


def task_emoji(title: str) -> str:
    """Return an emoji matching a keyword in the task title (default 🐾)."""
    lowered = title.lower()
    for keyword, emoji in TASK_EMOJI.items():
        if keyword in lowered:
            return emoji
    return "🐾"


def format_schedule(scheduler: Scheduler, plan) -> str:
    """Return the daily plan as a clean, emoji-annotated table."""
    rows = [
        [
            item.start_time,
            f"{task_emoji(item.task.title)} {item.task.title}",
            item.pet.name,
            f"{item.task.duration_minutes} min",
            f"{PRIORITY_EMOJI.get(item.task.priority, '')} {item.task.priority}",
        ]
        for item in plan.items
    ]
    headers = ["Time", "Task", "Pet", "Duration", "Priority"]
    return tabulate(rows, headers=headers, tablefmt="rounded_outline")


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

    plan = scheduler.build_daily_plan(owner)
    print(f"📅 Daily plan for {owner.name}'s pets:\n")
    print(format_schedule(scheduler, plan))


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
