from datetime import datetime, timedelta
from typing import List


class Task:
    """Represents a single activity."""
    
    def __init__(self):
        self.description: str = ""
        self.time: datetime = None
        self.frequency: str = ""
        self.completion_status: bool = False
    
    def mark_completed(self) -> None:
        """Mark this task as completed."""
        self.completion_status = True
    
    def is_overdue(self) -> bool:
        """Check if this task is overdue."""
        if self.time and not self.completion_status:
            return datetime.now() > self.time
        return False


class Pet:
    """Stores pet details and a list of tasks."""
    
    def __init__(self):
        self.name: str = ""
        self.species: str = ""
        self.breed: str = ""
        self.age: int = 0
        self.health_notes: str = ""
        self.tasks: List[Task] = []
    
    def add_task(self, task: Task) -> None:
        """Add a task for this pet."""
        self.tasks.append(task)
    
    def get_tasks(self) -> List[Task]:
        """Retrieve all tasks for this pet."""
        return self.tasks


class Owner:
    """Manages multiple pets and provides access to all their tasks."""
    
    def __init__(self):
        self.name: str = ""
        self.email: str = ""
        self.pets: List[Pet] = []
    
    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's collection."""
        self.pets.append(pet)
    
    def get_pets(self) -> List[Pet]:
        """Retrieve all pets owned by this owner."""
        return self.pets
    
    def get_all_tasks(self) -> List[Task]:
        """Retrieve all tasks from all pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks


class Scheduler:
    """The 'Brain' that retrieves, organizes, and manages tasks across pets."""
    
    def __init__(self, owner: Owner):
        self.owner = owner
    
    def retrieve_tasks(self) -> List[Task]:
        """Retrieve all tasks from the owner."""
        return self.owner.get_all_tasks()
    
    def organize_tasks(self, tasks: List[Task]) -> List[Task]:
        """Organize tasks, e.g., sort by time or priority."""
        # For simplicity, sort by time
        return sorted(tasks, key=lambda t: t.time or datetime.max)

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by their time in HH:MM format."""
        return sorted(
            tasks,
            key=lambda t: t.time.strftime("%H:%M") if t.time else "99:99",
        )

    def get_pending_tasks(self, tasks: List[Task]) -> List[Task]:
        """Return only tasks that are not completed."""
        return [task for task in tasks if not task.completion_status]

    def mark_task_complete(self, task: Task) -> None:
        """Mark a task as complete and roll forward daily tasks."""
        task.mark_completed()

        if task.frequency.lower() == "daily":
            next_task = Task()
            next_task.description = task.description
            next_task.frequency = task.frequency
            next_task.time = task.time + timedelta(days=1) if task.time else None
            # keep completion status as False for the next occurrence
            next_task.completion_status = False
            self.owner.pets[0].add_task(next_task) if self.owner.pets else None

    def check_conflicts(self) -> List[str]:
        """Detect overlapping tasks for the same pet at the same time."""
        warnings: List[str] = []
        for pet in self.owner.pets:
            # group tasks by timestamp (only exact same datetime values are considered overlaps)
            tasks_by_time = {}
            for task in pet.tasks:
                if task.time is None:
                    continue
                key = task.time
                tasks_by_time.setdefault(key, []).append(task)

            for time_point, tasks_in_slot in tasks_by_time.items():
                if len(tasks_in_slot) > 1:
                    descriptions = ", ".join([t.description for t in tasks_in_slot])
                    warning = (
                        f"Conflict for pet '{pet.name}' at {time_point.strftime('%Y-%m-%d %H:%M')}: "
                        f"{descriptions}"
                    )
                    warnings.append(warning)

        return warnings

    def manage_tasks(self) -> None:
        """Manage tasks, e.g., check for overdue tasks."""
        tasks = self.retrieve_tasks()
        for task in tasks:
            if task.is_overdue():
                print(f"Task '{task.description}' is overdue!")

