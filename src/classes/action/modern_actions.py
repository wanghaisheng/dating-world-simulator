from __future__ import annotations
from typing import TYPE_CHECKING, Optional

from src.classes.action.action import Action
from src.classes.action_runtime import ActionResult, ActionStatus

if TYPE_CHECKING:
    from src.classes.avatar import Avatar
    from src.classes.world import World

class ModernAction(Action):
    """
    Base class for modern actions.
    """
    def __init__(self, avatar: Avatar, world: World):
        super().__init__(avatar, world)

    def execute(self) -> ActionResult:
        return ActionResult(success=True, status=ActionStatus.SUCCESS, message="Modern action executed.")

class WorkAction(ModernAction):
    """
    Action for working.
    """
    def execute(self) -> ActionResult:
        if hasattr(self.avatar, "modern_profile") and self.avatar.modern_profile:
             self.avatar.update_modern_status(stress_delta=5, energy_delta=-10)
             self.avatar.modern_profile.monthly_income += 100 # Simplified
        return ActionResult(success=True, status=ActionStatus.SUCCESS, message="Worked hard.")

class SleepAction(ModernAction):
    """
    Action for sleeping.
    """
    def execute(self) -> ActionResult:
        if hasattr(self.avatar, "modern_profile") and self.avatar.modern_profile:
             self.avatar.modern_profile.energy = 100 # Reset to full? Or just +delta?
             # Using update_modern_status for stress, but energy sets to full usually on sleep
             self.avatar.update_modern_status(stress_delta=-20)
             # Manually set energy to max if that's the logic, or use large delta
             self.avatar.modern_profile.energy = 100
        return ActionResult(success=True, status=ActionStatus.SUCCESS, message="Slept well.")

class LeisureAction(ModernAction):
    """
    Action for leisure/relaxing.
    """
    def execute(self) -> ActionResult:
        if hasattr(self.avatar, "modern_profile") and self.avatar.modern_profile:
             self.avatar.update_modern_status(stress_delta=-10, mood_delta=10)
        return ActionResult(success=True, status=ActionStatus.SUCCESS, message="Enjoyed leisure time.")

class StudyAction(ModernAction):
    """
    Action for studying.
    """
    def execute(self) -> ActionResult:
        if hasattr(self.avatar, "modern_profile") and self.avatar.modern_profile:
             self.avatar.update_modern_status(stress_delta=5, energy_delta=-5)
        return ActionResult(success=True, status=ActionStatus.SUCCESS, message="Studied.")

class CommuteAction(ModernAction):
    """
    Action for commuting.
    """
    def execute(self) -> ActionResult:
        if hasattr(self.avatar, "modern_profile") and self.avatar.modern_profile:
             self.avatar.update_modern_status(stress_delta=2, energy_delta=-2)
        return ActionResult(success=True, status=ActionStatus.SUCCESS, message="Commuted.")
