import streamlit as st
from datetime import datetime, timedelta
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

if "owner" not in st.session_state:
    st.session_state.owner = Owner()

# keep owner info in sync with UI inputs
st.session_state.owner.name = owner_name

# Track current pet
if "current_pet" not in st.session_state:
    st.session_state.current_pet = None

if st.button("Add Pet"):
    pet = Pet()
    pet.name = pet_name
    pet.species = species
    st.session_state.owner.add_pet(pet)
    st.session_state.current_pet = pet
    st.success(f"Added {pet_name} ({species}) to owner {owner_name}.")

st.markdown("### Tasks")
st.caption("Add tasks to the selected pet. They will be sorted chronologically and checked for conflicts.")

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    task_hour = st.number_input("Hour (0-23)", min_value=0, max_value=23, value=8)
with col3:
    task_minute = st.number_input("Minute (0-59)", min_value=0, max_value=59, value=0)

if st.button("Add task"):
    if st.session_state.owner.get_pets():
        # Use the first pet or current pet
        pet = st.session_state.current_pet or st.session_state.owner.get_pets()[0]
        
        # Create a Task object
        new_task = Task()
        new_task.description = task_title
        new_task.time = datetime.now().replace(hour=task_hour, minute=task_minute, second=0, microsecond=0)
        new_task.frequency = "daily"
        
        pet.add_task(new_task)
        st.success(f"Added '{task_title}' at {task_hour:02d}:{task_minute:02d}")
    else:
        st.error("Please add a pet first.")

# Display tasks from all pets
if st.session_state.owner.get_pets():
    st.write("### Current Tasks (sorted by time)")
    
    scheduler = Scheduler(st.session_state.owner)
    all_tasks = scheduler.retrieve_tasks()
    
    if all_tasks:
        # Sort tasks by time
        sorted_tasks = scheduler.sort_by_time(all_tasks)
        
        # Check for conflicts
        conflicts = scheduler.check_conflicts()
        if conflicts:
            for conflict in conflicts:
                st.warning(f"⚠️ {conflict}")
        
        # Display sorted tasks
        task_data = []
        for task in sorted_tasks:
            time_str = task.time.strftime("%H:%M") if task.time else "No time set"
            status = "✅ Done" if task.completion_status else "⏳ Pending"
            task_data.append({
                "Time": time_str,
                "Task": task.description,
                "Frequency": task.frequency,
                "Status": status
            })
        
        st.table(task_data)
    else:
        st.info("No tasks yet. Add one above.")
else:
    st.info("Add a pet first to start creating tasks.")

st.divider()

st.subheader("Build Schedule")
st.caption("Generate and review your complete daily schedule.")

if st.button("Generate schedule"):
    if st.session_state.owner.get_pets():
        scheduler = Scheduler(st.session_state.owner)
        all_tasks = scheduler.retrieve_tasks()
        
        if all_tasks:
            st.subheader("📅 Today's Schedule")
            sorted_tasks = scheduler.sort_by_time(all_tasks)
            
            # Check and display conflicts
            conflicts = scheduler.check_conflicts()
            if conflicts:
                st.subheader("⚠️ Scheduling Conflicts Detected")
                for conflict in conflicts:
                    st.warning(conflict)
            else:
                st.success("✅ No scheduling conflicts!")
            
            # Display organized schedule
            st.subheader("🕐 Tasks by Time")
            for task in sorted_tasks:
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.caption(task.time.strftime("%H:%M") if task.time else "Unscheduled")
                with col2:
                    st.write(f"**{task.description}** ({task.frequency})")
        else:
            st.warning("No tasks added yet. Add some tasks to generate a schedule.")
    else:
        st.error("Please add a pet and tasks first.")
