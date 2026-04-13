from dataclasses import dataclass, field
from typing import List, Optional, TYPE_CHECKING, Dict
from enum import Enum

if TYPE_CHECKING:
    from src.classes.avatar.core import Avatar

class RelationshipStage(Enum):
    STRANGER = 0      # Affection < 10
    ACQUAINTANCE = 1  # 10 <= Affection < 30
    FRIEND = 2        # 30 <= Affection < 60
    CRUSH = 3         # 60 <= Affection < 80
    LOVER = 4         # 80 <= Affection
    PARTNER = 5       # Engaged/Married
    EX = -1           # Ex-partner

@dataclass
class ModernProfile:
    """
    Data container for Modern Urban Romance simulation.
    Contains attributes specific to modern setting like occupation, MBTI, relationships, etc.
    """
    # Basic Profile
    occupation: str = "Unemployed"
    education: str = "Unknown"
    mbti: str = "ISTJ"
    hobbies: List[str] = field(default_factory=list)
    fashion_style: str = "Casual"
    
    # Financial & Status
    monthly_income: int = 0
    assets: int = 0
    social_status: int = 0  # 0-100
    
    # Relationship Status
    relationship_status: str = "Single"  # Single, Dating, Complicated, Married
    crush_on: Optional[str] = None  # ID of the avatar they have a crush on
    jealousy_threshold: float = 50.0  # 0-100
    relationships: Dict[str, dict] = field(default_factory=dict) # Tracks specific state with each person
    
    # Dynamic State
    energy: int = 100  # 0-100, daily energy
    stress: int = 0    # 0-100
    mood: int = 50     # 0-100
    
    # Hidden Traits
    sincerity: int = 80      # 0-100, default high, lower for antagonists
    hidden_archetype: Optional[str] = None  # None, "GOLD_DIGGER", "NPD", "SCAMMER", "PLAYER", "PUA"
    
    # Schedule
    daily_schedule: dict[int, str] = field(default_factory=dict) # {hour: activity}

class ModernProfileMixin:
    """
    Mixin for Modern Urban Romance simulation methods.
    Assumes self has a 'modern_profile' attribute of type Optional[ModernProfile].
    """
    
    def ensure_modern_profile(self: "Avatar") -> None:
        """Ensure the avatar has a modern profile initialized."""
        if self.modern_profile is None:
            self.modern_profile = ModernProfile()

    def get_relationship_stage(self: "Avatar", target: "Avatar") -> RelationshipStage:
        """Calculate relationship stage based on affection and status."""
        self.ensure_modern_profile()
        
        # Get data from modern profile relationships map
        # relationships is Dict[str, dict] where key is target.id
        rel_data = self.modern_profile.relationships.get(target.id, {})
        affection = rel_data.get("affection", 0)
        
        # Check explicit status first (if needed in future)
        # explicit_status = rel_data.get("status")
        
        if affection < 10:
            return RelationshipStage.STRANGER
        elif affection < 30:
            return RelationshipStage.ACQUAINTANCE
        elif affection < 60:
            return RelationshipStage.FRIEND
        elif affection < 80:
            return RelationshipStage.CRUSH
        else:
            return RelationshipStage.LOVER

    def generate_daily_schedule(self: "Avatar") -> None:
        """Generate a new daily schedule."""
        from src.classes.modern.schedule import ScheduleGenerator
        
        self.ensure_modern_profile()
        self.modern_profile.daily_schedule = ScheduleGenerator.generate(self)

    def get_scheduled_activity(self: "Avatar", hour: int) -> str:
        """Get the activity planned for the given hour."""
        if not self.modern_profile or not self.modern_profile.daily_schedule:
            return "Idle"
            
        return self.modern_profile.daily_schedule.get(hour, "Idle")

    def update_modern_status(self: "Avatar", energy_delta: int = 0, stress_delta: int = 0, mood_delta: int = 0) -> None:
        """Update dynamic status (energy, stress, mood) with clamping."""
        self.ensure_modern_profile()
        mp = self.modern_profile
        
        # Update Energy
        mp.energy = max(0, min(100, mp.energy + energy_delta))
        
        # Update Stress
        mp.stress = max(0, min(100, mp.stress + stress_delta))
        
        # Update Mood
        mp.mood = max(0, min(100, mp.mood + mood_delta))

    def get_modern_occupation(self: "Avatar") -> str:
        if self.modern_profile:
            return self.modern_profile.occupation
        return "Unknown"

    def update_modern_status(self: "Avatar", energy_delta: int = 0, stress_delta: int = 0, mood_delta: int = 0) -> None:
        """Update dynamic status values with clamping."""
        if not self.modern_profile:
            return
            
        p = self.modern_profile
        p.energy = max(0, min(100, p.energy + energy_delta))
        p.stress = max(0, min(100, p.stress + stress_delta))
        p.mood = max(0, min(100, p.mood + mood_delta))

    def is_tired(self: "Avatar") -> bool:
        """Check if avatar is too tired to act."""
        if not self.modern_profile:
            return False
        return self.modern_profile.energy < 20

    def get_schedule_preference(self: "Avatar") -> str:
        """Get schedule type based on occupation/traits."""
        if not self.modern_profile:
            return "standard"
            
        occ = self.modern_profile.occupation.lower()
        if "student" in occ:
            return "student"
        if "ceo" in occ or "founder" in occ:
            return "workaholic"
        if "freelancer" in occ:
            return "flexible"
        return "standard"
