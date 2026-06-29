"""CLI demo for PawPal+: builds a sample owner/pets/tasks and prints today's schedule."""

from pawpal_system import Owner, Pet, Task, Scheduler


def main() -> None:
    owner = Owner(name="Jordan")

    biscuit = owner.add_pet(Pet(name="Biscuit", species="dog"))
    mochi = owner.add_pet(Pet(name="Mochi", species="cat"))

    biscuit.add_task(Task("Morning walk", 30, priority="high", preferred_time="08:00"))
    biscuit.add_task(Task("Feeding", 10, priority="high", preferred_time="09:00"))
    biscuit.add_task(Task("Enrichment play", 20, priority="low"))
    mochi.add_task(Task("Feeding", 10, priority="high"))
    mochi.add_task(Task("Litter cleanup", 15, priority="medium"))

    scheduler = Scheduler(start_time="08:00", available_minutes=480)
    plan = scheduler.build_daily_plan(owner)

    print(f"Daily plan for {owner.name}'s pets:\n")
    print(scheduler.explain_plan(plan))
    print(f"\nTotal scheduled: {plan.total_minutes()} min "
          f"({len(plan.items)} tasks, {len(plan.skipped)} skipped)")


if __name__ == "__main__":
    main()
