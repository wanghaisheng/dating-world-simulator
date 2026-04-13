from __future__ import annotations
from typing import TYPE_CHECKING, Dict, List
import random

if TYPE_CHECKING:
    from src.classes.avatar import Avatar

class ScheduleGenerator:
    """
    Generates daily schedules for avatars in Modern Romance mode.
    """
    
    @staticmethod
    def generate(avatar: "Avatar") -> Dict[int, str]:
        """
        Generates a 24-hour schedule based on avatar's occupation and traits.
        Returns a dict {hour (0-23): activity_name}
        """
        schedule = {}
        avatar.ensure_modern_profile()
        occupation = avatar.modern_profile.occupation if avatar.modern_profile else "Unemployed"
        
        # Default schedule (Unemployed)
        # Sleep: 23:00 - 07:00
        # Leisure: 08:00 - 22:00
        
        # Basic Sleep
        for h in range(0, 7):
            schedule[h] = "Sleep"
        for h in range(23, 24):
            schedule[h] = "Sleep"
            
        if occupation == "Student":
            # Study: 08:00 - 16:00
            for h in range(8, 17):
                schedule[h] = "Study"
            # Commute
            schedule[7] = "Commute"
            schedule[17] = "Commute"
            # Leisure
            for h in range(18, 23):
                schedule[h] = "Leisure"
                
        elif occupation in ["Office Worker", "Programmer", "Teacher", "Doctor"]:
            # Work: 09:00 - 18:00
            for h in range(9, 18):
                schedule[h] = "Work"
            # Commute
            schedule[8] = "Commute"
            schedule[18] = "Commute"
            # Leisure
            schedule[7] = "Leisure"
            for h in range(19, 23):
                schedule[h] = "Leisure"
                
        else:
            # Unemployed / Freelance / Others
            # Mostly Leisure
            for h in range(7, 23):
                schedule[h] = "Leisure"
                
        return schedule
