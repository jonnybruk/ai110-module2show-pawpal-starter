from datetime import datetime, timedelta

from pawpal_system import Pet, Task, Owner, Scheduler


def test_task_completion_marks_as_completed():
    task = Task()
    task.description = "Water the plants"
    task.time = datetime.now() + timedelta(hours=1)
    task.frequency = "daily"
    assert task.completion_status is False

    task.mark_completed()

    assert task.completion_status is True


def test_pet_task_addition_increases_task_count():
    pet = Pet()
    pet.name = "Finn"

    initial_tasks = len(pet.get_tasks())
    assert initial_tasks == 0

    new_task = Task()
    new_task.description = "Evening walk"
    new_task.time = datetime.now() + timedelta(hours=2)

    pet.add_task(new_task)

    assert len(pet.get_tasks()) == initial_tasks + 1


# ============================================================================
# TESTS: Sorting Tasks Chronologically
# ============================================================================

def test_sort_by_time_orders_tasks_chronologically():
    """Tasks should be sorted by time in HH:MM format."""
    owner = Owner()
    scheduler = Scheduler(owner)
    
    # Create tasks with different times
    task_morning = Task()
    task_morning.description = "Morning walk"
    task_morning.time = datetime(2026, 3, 31, 8, 0)
    
    task_evening = Task()
    task_evening.description = "Evening walk"
    task_evening.time = datetime(2026, 3, 31, 18, 0)
    
    task_noon = Task()
    task_noon.description = "Lunch break"
    task_noon.time = datetime(2026, 3, 31, 12, 0)
    
    # Add in non-chronological order
    tasks = [task_evening, task_morning, task_noon]
    sorted_tasks = scheduler.sort_by_time(tasks)
    
    # Verify chronological order
    assert sorted_tasks[0].description == "Morning walk"
    assert sorted_tasks[1].description == "Lunch break"
    assert sorted_tasks[2].description == "Evening walk"


def test_sort_by_time_handles_none_times():
    """Tasks with None time should sort to the end."""
    owner = Owner()
    scheduler = Scheduler(owner)
    
    task_with_time = Task()
    task_with_time.description = "Scheduled task"
    task_with_time.time = datetime(2026, 3, 31, 10, 0)
    
    task_no_time = Task()
    task_no_time.description = "Unscheduled task"
    task_no_time.time = None
    
    tasks = [task_no_time, task_with_time]
    sorted_tasks = scheduler.sort_by_time(tasks)
    
    # Scheduled task should come first, unscheduled last
    assert sorted_tasks[0].description == "Scheduled task"
    assert sorted_tasks[1].description == "Unscheduled task"


def test_sort_by_time_preserves_order_for_same_time():
    """Tasks with same time should maintain insertion order (stable sort)."""
    owner = Owner()
    scheduler = Scheduler(owner)
    
    same_time = datetime(2026, 3, 31, 14, 30)
    
    task1 = Task()
    task1.description = "Task A"
    task1.time = same_time
    
    task2 = Task()
    task2.description = "Task B"
    task2.time = same_time
    
    task3 = Task()
    task3.description = "Task C"
    task3.time = same_time
    
    tasks = [task1, task2, task3]
    sorted_tasks = scheduler.sort_by_time(tasks)
    
    # Order should be preserved
    assert sorted_tasks[0].description == "Task A"
    assert sorted_tasks[1].description == "Task B"
    assert sorted_tasks[2].description == "Task C"


def test_organize_tasks_sorts_chronologically_with_full_datetime():
    """organize_tasks should sort by full datetime, including dates."""
    owner = Owner()
    scheduler = Scheduler(owner)
    
    # Tasks on different days
    task_today = Task()
    task_today.description = "Today"
    task_today.time = datetime(2026, 3, 31, 15, 0)
    
    task_tomorrow = Task()
    task_tomorrow.description = "Tomorrow"
    task_tomorrow.time = datetime(2026, 4, 1, 9, 0)
    
    task_yesterday = Task()
    task_yesterday.description = "Yesterday"
    task_yesterday.time = datetime(2026, 3, 30, 18, 0)
    
    tasks = [task_today, task_tomorrow, task_yesterday]
    organized = scheduler.organize_tasks(tasks)
    
    # Should be chronologically ordered by full datetime
    assert organized[0].description == "Yesterday"
    assert organized[1].description == "Today"
    assert organized[2].description == "Tomorrow"


def test_sort_by_time_empty_list():
    """Sorting empty task list should return empty list."""
    owner = Owner()
    scheduler = Scheduler(owner)
    
    sorted_tasks = scheduler.sort_by_time([])
    
    assert sorted_tasks == []


# ============================================================================
# TESTS: Completing Daily Tasks Creates Next Day Task
# ============================================================================

def test_mark_task_complete_daily_creates_next_task():
    """Completing a daily task should create a new task for tomorrow."""
    owner = Owner()
    pet = Pet()
    pet.name = "Buddy"
    owner.add_pet(pet)
    
    # Create a daily task
    tomorrow_morning = datetime.now() + timedelta(days=1)
    task = Task()
    task.description = "Morning walk"
    task.time = tomorrow_morning.replace(hour=8, minute=0)
    task.frequency = "daily"
    pet.add_task(task)
    
    scheduler = Scheduler(owner)
    initial_count = len(pet.get_tasks())
    
    # Complete the task
    scheduler.mark_task_complete(task)
    
    # Should have one more task now
    assert len(pet.get_tasks()) == initial_count + 1
    
    # New task should be for tomorrow (24 hours later)
    new_task = pet.get_tasks()[-1]
    assert new_task.description == "Morning walk"
    assert new_task.frequency == "daily"
    assert new_task.completion_status is False
    assert new_task.time.day == task.time.day + 1


def test_mark_task_complete_daily_advances_time_correctly():
    """New daily task should be scheduled exactly 24 hours later."""
    owner = Owner()
    pet = Pet()
    pet.name = "Mittens"
    owner.add_pet(pet)
    
    original_time = datetime(2026, 3, 31, 14, 30, 0)
    task = Task()
    task.description = "Feed cat"
    task.time = original_time
    task.frequency = "daily"
    pet.add_task(task)
    
    scheduler = Scheduler(owner)
    scheduler.mark_task_complete(task)
    
    new_task = pet.get_tasks()[-1]
    expected_time = original_time + timedelta(days=1)
    
    assert new_task.time == expected_time


def test_mark_task_complete_non_daily_does_not_recur():
    """Completing a non-daily task should not create a new task."""
    owner = Owner()
    pet = Pet()
    pet.name = "Buddy"
    owner.add_pet(pet)
    
    task = Task()
    task.description = "Annual vet checkup"
    task.time = datetime.now() + timedelta(days=1)
    task.frequency = "once"
    pet.add_task(task)
    
    scheduler = Scheduler(owner)
    initial_count = len(pet.get_tasks())
    
    scheduler.mark_task_complete(task)
    
    # Task count should not increase
    assert len(pet.get_tasks()) == initial_count


def test_mark_task_complete_none_time_stays_none():
    """Completing a daily task with None time should preserve None for next task."""
    owner = Owner()
    pet = Pet()
    pet.name = "Buddy"
    owner.add_pet(pet)
    
    task = Task()
    task.description = "Sometime task"
    task.time = None
    task.frequency = "daily"
    pet.add_task(task)
    
    scheduler = Scheduler(owner)
    scheduler.mark_task_complete(task)
    
    new_task = pet.get_tasks()[-1]
    
    # New task should also have None time
    assert new_task.time is None
    assert new_task.frequency == "daily"
    assert new_task.completion_status is False


def test_mark_task_complete_case_insensitive_daily():
    """Daily task recognition should be case-insensitive."""
    owner = Owner()
    pet = Pet()
    pet.name = "Buddy"
    owner.add_pet(pet)
    
    task = Task()
    task.description = "Feed dog"
    task.time = datetime.now() + timedelta(days=1)
    task.frequency = "DAILY"  # Uppercase
    pet.add_task(task)
    
    scheduler = Scheduler(owner)
    initial_count = len(pet.get_tasks())
    
    scheduler.mark_task_complete(task)
    
    # Should create a new task despite uppercase frequency
    assert len(pet.get_tasks()) == initial_count + 1


def test_mark_task_complete_marks_original_as_done():
    """mark_task_complete should set the original task's completion_status to True."""
    owner = Owner()
    pet = Pet()
    pet.name = "Buddy"
    owner.add_pet(pet)
    
    task = Task()
    task.description = "Walk"
    task.time = datetime.now() + timedelta(days=1)
    task.frequency = "daily"
    pet.add_task(task)
    
    assert task.completion_status is False
    
    scheduler = Scheduler(owner)
    scheduler.mark_task_complete(task)
    
    assert task.completion_status is True


# ============================================================================
# TESTS: Overlapping Times Trigger Conflict Warnings
# ============================================================================

def test_check_conflicts_detects_overlapping_tasks():
    """Tasks at the same time for the same pet should trigger a conflict warning."""
    owner = Owner()
    pet = Pet()
    pet.name = "Buddy"
    owner.add_pet(pet)
    
    same_time = datetime(2026, 3, 31, 9, 0)
    
    task1 = Task()
    task1.description = "Morning walk"
    task1.time = same_time
    
    task2 = Task()
    task2.description = "Feed breakfast"
    task2.time = same_time
    
    pet.add_task(task1)
    pet.add_task(task2)
    
    scheduler = Scheduler(owner)
    warnings = scheduler.check_conflicts()
    
    # Should have at least one conflict warning
    assert len(warnings) > 0
    assert "Conflict" in warnings[0]
    assert "Buddy" in warnings[0]
    assert "09:00" in warnings[0]


def test_check_conflicts_multiple_overlaps():
    """Multiple tasks at the same time should appear in one conflict message."""
    owner = Owner()
    pet = Pet()
    pet.name = "Mittens"
    owner.add_pet(pet)
    
    overlap_time = datetime(2026, 3, 31, 14, 0)
    
    task1 = Task()
    task1.description = "Grooming"
    task1.time = overlap_time
    
    task2 = Task()
    task2.description = "Play session"
    task2.time = overlap_time
    
    task3 = Task()
    task3.description = "Training"
    task3.time = overlap_time
    
    pet.add_task(task1)
    pet.add_task(task2)
    pet.add_task(task3)
    
    scheduler = Scheduler(owner)
    warnings = scheduler.check_conflicts()
    
    # Should detect 3 tasks at same time
    assert len(warnings) > 0
    warning = warnings[0]
    assert "Grooming" in warning
    assert "Play session" in warning
    assert "Training" in warning


def test_check_conflicts_no_warning_for_different_times():
    """Tasks at different times should not trigger warnings."""
    owner = Owner()
    pet = Pet()
    pet.name = "Buddy"
    owner.add_pet(pet)
    
    task1 = Task()
    task1.description = "Morning walk"
    task1.time = datetime(2026, 3, 31, 8, 0)
    
    task2 = Task()
    task2.description = "Evening walk"
    task2.time = datetime(2026, 3, 31, 18, 0)
    
    pet.add_task(task1)
    pet.add_task(task2)
    
    scheduler = Scheduler(owner)
    warnings = scheduler.check_conflicts()
    
    # Should have no conflicts
    assert len(warnings) == 0


def test_check_conflicts_ignores_none_times():
    """Tasks with None time should not trigger conflicts."""
    owner = Owner()
    pet = Pet()
    pet.name = "Buddy"
    owner.add_pet(pet)
    
    task1 = Task()
    task1.description = "Unscheduled task 1"
    task1.time = None
    
    task2 = Task()
    task2.description = "Unscheduled task 2"
    task2.time = None
    
    pet.add_task(task1)
    pet.add_task(task2)
    
    scheduler = Scheduler(owner)
    warnings = scheduler.check_conflicts()
    
    # Should have no conflicts because None times are excluded
    assert len(warnings) == 0


def test_check_conflicts_per_pet_isolation():
    """Conflicts should only be reported for the affected pet."""
    owner = Owner()
    
    pet1 = Pet()
    pet1.name = "Buddy"
    owner.add_pet(pet1)
    
    pet2 = Pet()
    pet2.name = "Mittens"
    owner.add_pet(pet2)
    
    conflict_time = datetime(2026, 3, 31, 10, 0)
    
    # Task 1 and 2 for pet1 at same time
    task1 = Task()
    task1.description = "Walk"
    task1.time = conflict_time
    pet1.add_task(task1)
    
    task2 = Task()
    task2.description = "Feed"
    task2.time = conflict_time
    pet1.add_task(task2)
    
    # Task 3 for pet2 at same time (should NOT conflict)
    task3 = Task()
    task3.description = "Playtime"
    task3.time = conflict_time
    pet2.add_task(task3)
    
    scheduler = Scheduler(owner)
    warnings = scheduler.check_conflicts()
    
    # Should have exactly 1 warning (for pet1 only)
    assert len(warnings) == 1
    assert "Buddy" in warnings[0]
    assert "Mittens" not in warnings[0]


def test_check_conflicts_same_time_different_dates():
    """Same time on different dates should NOT conflict (only exact match matters)."""
    owner = Owner()
    pet = Pet()
    pet.name = "Buddy"
    owner.add_pet(pet)
    
    task1 = Task()
    task1.description = "Walk March 31"
    task1.time = datetime(2026, 3, 31, 9, 0)
    
    task2 = Task()
    task2.description = "Walk April 1"
    task2.time = datetime(2026, 4, 1, 9, 0)  # Different date, same time
    
    pet.add_task(task1)
    pet.add_task(task2)
    
    scheduler = Scheduler(owner)
    warnings = scheduler.check_conflicts()
    
    # Should have no conflicts (different dates)
    assert len(warnings) == 0


def test_check_conflicts_empty_owner():
    """check_conflicts should handle owner with no pets gracefully."""
    owner = Owner()
    scheduler = Scheduler(owner)
    
    warnings = scheduler.check_conflicts()
    
    # Should return empty list without error
    assert warnings == []
