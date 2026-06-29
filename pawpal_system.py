"""PawPal+ logic layer: backend classes for owners, pets, tasks, and scheduling."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str = "medium"
    frequency: str = "daily"
    preferred_time: Optional[str] = None
    completed: bool = False

    def mark_complete(self) -> None: ...
    def reset(self) -> None: ...


@dataclass
class Pet:
    name: str
    species: str = "dog"
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> Task: ...
    def task_count(self) -> int: ...


@dataclass
class Owner:
    name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> Pet: ...
    def get_all_tasks(self) -> List[Task]: ...


class Scheduler:
    def __init__(self, start_time: str = "08:00", available_minutes: int = 480): ...
    def build_daily_plan(self, owner: Owner): ...
    def explain_plan(self, plan) -> str: ...
