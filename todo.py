from abc import ABC, abstractmethod

class TaskInterface(ABC):
    @abstractmethod
    def mark_done(self):
        """Mark this task as completed"""
        pass

    @abstractmethod
    def __str__(self):
        """Return a user-friendly string representation"""
        pass


class Task(TaskInterface):
    def __init__(self, title: str, priority: int = 3):
        """Create a new task with a title and priority (1=high, 5=low)"""
        self.title = title
        self.priority = priority
        self.done = False

    def mark_done(self):
        """Mark this task as completed"""
        self.done = True
        return True

    def __str__(self):
        """Return a user-friendly string representation"""
        return f"[{'x' if self.done else ' '}] {self.title} (Priority {self.priority})"


class TodoList:
    def __init__(self):
        """Initialize an empty todo list"""
        self.tasks = []

    def add_task(self, *tasks: TaskInterface):
        """Add one or more tasks"""
        for task in tasks:
            self.tasks.append(task)

    def remove_task(self, index: int):
        """Remove a task by index"""
        if 0 <= index < len(self.tasks):
            removed = self.tasks.pop(index)
            return removed
        else:
            print("Invalid index")
            return None

    def list_tasks(self, show_all: bool = True):
        """List tasks, optionally filtering completed ones"""
        for i, task in enumerate(self.tasks):
            if show_all or not task.done:
                print(f"{i + 1}. {task}")

    def is_empty(self) -> bool:
        """Return True if no tasks are stored"""
        return len(self.tasks) == 0

    def get_pending_tasks(self) -> list:
        """Return a list of incomplete tasks"""
        return [task for task in self.tasks if not task.done]

    def load_tasks_from_dicts(self, task_data: list[dict]):
        """Create and load tasks from a list of dicts"""
        for data in task_data:
            title = data.get("title", "Untitled")
            priority = data.get("priority", 3)
            self.add_task(Task(title, priority))


def main():
    """Simple test run"""
    todo = TodoList()
    todo.add_task(Task("Read a book", 2), Task("Go jogging", 4))
    todo.list_tasks()
    print("Pending:", len(todo.get_pending_tasks()))
