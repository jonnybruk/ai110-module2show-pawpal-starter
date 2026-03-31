from datetime import datetime, timedelta

from pawpal_system import Pet, Task


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
