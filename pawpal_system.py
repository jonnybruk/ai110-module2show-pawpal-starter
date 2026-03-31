from datetime import datetime
from typing import List


class Owner:
    """Represents a pet owner."""
    
    def __init__(self):
        self.name: str = ""
        self.email: str = ""
        self.pets: List[Pet] = []
    
    def add_pet(self, pet: 'Pet') -> None:
        """Add a pet to the owner's collection."""
        pass
    
    def get_pets(self) -> List['Pet']:
        """Retrieve all pets owned by this owner."""
        pass


class Pet:
    """Represents a pet."""
    
    def __init__(self):
        self.name: str = ""
        self.species: str = ""
        self.breed: str = ""
        self.age: int = 0
        self.health_notes: str = ""
        self.tasks: List[Task] = []
    
    def add_task(self, task: 'Task') -> None:
        """Add a task for this pet."""
        pass
    
    def get_tasks(self) -> List['Task']:
        """Retrieve all tasks for this pet."""
        pass


class Task:
    """Represents a pet care task."""
    
    def __init__(self):
        self.type: str = ""  # walk, feeding, meds, grooming, enrichment
        self.duration_minutes: int = 0
        self.priority: int = 0
        self.due_time: datetime = None
        self.is_completed: bool = False
    
    def mark_completed(self) -> None:
        """Mark this task as completed."""
        pass
    
    def is_overdue(self) -> bool:
        """Check if this task is overdue."""
        pass


class Constraint:
    """Represents scheduling constraints for the planner."""
    
    def __init__(self):
        self.available_minutes: int = 0
        self.preferences: List[str] = []
        self.blocked_times: List[datetime] = []
    
    def fits(self, task: Task) -> bool:
        """Check if a task fits within the constraints."""
        pass
    
    def explain_fit(self, task: Task) -> str:
        """Explain why or why not a task fits the constraints."""
        pass


class DailyPlanner:
    """Generates daily pet care plans based on constraints."""
    
    def __init__(self):
        self.selected_tasks: List[Task] = []
        self.reasoning: str = ""
    
    def generate_plan(self, pet: Pet, constraint: Constraint) -> None:
        """Generate a daily plan for a pet given constraints."""
        pass
    
    def rank_tasks(self, tasks: List[Task]) -> List[Task]:
        """Rank tasks by priority and other factors."""
        pass
    
    def explain_plan(self) -> str:
        """Provide an explanation of the generated plan."""
        pass
