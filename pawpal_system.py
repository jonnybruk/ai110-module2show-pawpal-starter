from datetime import datetime
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
    
    def manage_tasks(self) -> None:
        """Manage tasks, e.g., check for overdue tasks."""
        tasks = self.retrieve_tasks()
        for task in tasks:
            if task.is_overdue():
                print(f"Task '{task.description}' is overdue!")

