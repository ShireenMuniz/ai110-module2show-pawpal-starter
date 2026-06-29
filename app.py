import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
PawPal+ helps a pet owner plan daily care tasks for their pet(s) based on
constraints like time, priority, and preferences.
"""
)

with st.expander("Scenario", expanded=False):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. Add an owner and pets, give each pet
some care tasks, then generate a daily schedule that orders tasks by priority and
fits them into the time you have available.
"""
    )

st.divider()

# --- Application memory: keep one Owner across reruns ---
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan")

owner = st.session_state.owner

# --- Owner ---
st.subheader("Owner & Pets")
owner.name = st.text_input("Owner name", value=owner.name)

# --- Add a pet ---
with st.form("add_pet"):
    new_pet_name = st.text_input("Pet name", value="Mochi")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    if st.form_submit_button("Add pet"):
        owner.add_pet(Pet(name=new_pet_name, species=species))
        st.success(f"Added {new_pet_name}!")

if not owner.pets:
    st.info("No pets yet. Add one above.")
    st.stop()

# --- Add a task to a chosen pet ---
st.markdown("### Add a Task")
pet_names = [p.name for p in owner.pets]
chosen = st.selectbox("Which pet?", pet_names)
with st.form("add_task"):
    title = st.text_input("Task title", value="Morning walk")
    col1, col2, col3 = st.columns(3)
    with col1:
        duration = st.number_input("Duration (min)", 1, 240, 20)
    with col2:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
    with col3:
        preferred = st.text_input("Preferred time (HH:MM, optional)", value="")
    if st.form_submit_button("Add task"):
        pet = next(p for p in owner.pets if p.name == chosen)
        pet.add_task(
            Task(
                title=title,
                duration_minutes=int(duration),
                priority=priority,
                preferred_time=preferred or None,
            )
        )
        st.success(f"Added '{title}' to {chosen}!")

# --- Show current tasks ---
st.markdown("### Current Tasks")
rows = [
    {"pet": pet.name, "task": t.title, "min": t.duration_minutes, "priority": t.priority}
    for pet in owner.pets
    for t in pet.tasks
]
if rows:
    st.table(rows)
    with st.expander("View tasks sorted by time"):
        for t in Scheduler.sort_by_time(owner.get_all_tasks()):
            st.write(f"- **{t.preferred_time or '--:--'}** {t.title} · _{t.priority}_")

else:
    st.info("No tasks yet.")

st.divider()

# --- Generate schedule ---
st.subheader("Build Schedule")
available = st.number_input("Minutes available today", 30, 1440, 480)
if st.button("Generate schedule"):
    scheduler = Scheduler(start_time="08:00", available_minutes=int(available))

    # Surface conflicts first so the owner sees clashes before the plan.
    conflicts = scheduler.detect_conflicts(owner)
    if conflicts:
        for c in conflicts:
            st.warning(f"⚠️ {c}")

    plan = scheduler.build_daily_plan(owner)
    if plan.items:
        st.success(f"Planned {len(plan.items)} tasks · {plan.total_minutes()} min total")
        st.table([
            {
                "time": item.start_time,
                "task": item.task.title,
                "pet": item.pet.name,
                "min": item.task.duration_minutes,
                "priority": item.task.priority,
            }
            for item in plan.items
        ])
        with st.expander("Why this plan?"):
            for item in plan.items:
                st.caption(f"{item.start_time} — {item.task.title}: {item.reason}")
    else:
        st.info("No tasks to schedule yet.")

    if plan.skipped:
        st.warning("Skipped (didn't fit):")
        for pet, task, reason in plan.skipped:
            st.write(f"- {task.title} ({pet.name}) — {reason}")
