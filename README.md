# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

<!-- Make sure your screenshot file is in the repo; e.g., 'screenshot.png' at repo root -->
![PawPal+ App Screenshot](./screenshot.png)

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.


## Testing PawPal+
To ensure the system logic for pet owners and task scheduling is reliable, I implemented an automated test suite using `pytest`.

To verify the system, run the following command in the terminal:
`python -m pytest`

The current test suite verifies:
Task Completion: Ensuring tasks correctly update to "completed" status.
Task Addition: Verifying that adding a task correctly increments the owner's task count.
Etc

I'm feeling 5/5 stars confident because all tests passed.

## Features

### 🕐 Chronological Task Sorting
The system implements intelligent task organization using a time-based sorting algorithm that ensures tasks are presented in logical order throughout the day.

**Algorithm Details:**
- **Time Format Sorting**: Tasks are sorted by their scheduled time using HH:MM string comparison (e.g., "08:30" < "14:15")
- **Unscheduled Task Handling**: Tasks without a specific time (`time = None`) are automatically placed at the end of the schedule
- **Stable Sort**: When multiple tasks share the same time, their original insertion order is preserved
- **Implementation**: Uses Python's `sorted()` function with a custom key function that converts datetime objects to time strings

**Use Cases:**
- Daily schedule generation displays tasks from morning to evening
- Streamlit UI shows organized task tables sorted by time
- Helps pet owners visualize their complete care routine chronologically

### ⚠️ Conflict Detection System
The scheduler includes sophisticated conflict detection to prevent scheduling overlaps that could stress pets or overwhelm owners.

**Algorithm Details:**
- **Per-Pet Analysis**: Conflicts are detected separately for each pet (a dog and cat can have tasks at the same time)
- **Exact Time Matching**: Identifies tasks scheduled at the exact same datetime (second precision)
- **Grouping Strategy**: Uses a dictionary to group tasks by timestamp, then checks for multiple tasks per time slot
- **Exclusion Logic**: Tasks with `time = None` are excluded from conflict analysis (unscheduled tasks can't conflict)

**Detection Process:**
1. Iterate through each pet owned by the user
2. Group all scheduled tasks by their exact datetime value
3. Identify time slots with 2+ tasks
4. Generate descriptive warning messages for each conflict

**Output Format:**
```
Conflict for pet 'Buddy' at 2026-03-31 09:00: Morning walk, Feed breakfast
```

### 🔄 Daily Task Recurrence
The system automatically manages recurring daily tasks, ensuring consistent pet care routines without manual re-entry.

**Algorithm Details:**
- **Completion Trigger**: When `mark_task_complete()` is called on a task with `frequency = "daily"`
- **24-Hour Advancement**: New task is scheduled exactly 24 hours later using `timedelta(days=1)`
- **Property Preservation**: Description, frequency, and other attributes are copied to the new task
- **Status Reset**: New task starts with `completion_status = False` (ready for next day)
- **Case-Insensitive Matching**: Frequency comparison uses `.lower()` to handle "Daily", "DAILY", "daily"

**Recurrence Flow:**
1. Original task marked as completed
2. Check if `frequency.lower() == "daily"`
3. Create new Task object with identical properties
4. Advance time by 24 hours (preserves None time for unscheduled tasks)
5. Add new task to the pet's task list

**Edge Cases Handled:**
- Tasks with no scheduled time remain unscheduled in recurrence
- Empty pet lists are safely handled (no crash)
- Non-daily frequencies are ignored (no unwanted recurrence)

**Current Limitation:** New recurring tasks are always added to the first pet in the owner's list. Future enhancement could track which pet originally owned the task.


