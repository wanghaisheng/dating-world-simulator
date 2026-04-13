from typing import TYPE_CHECKING, List, Optional, Dict
from dataclasses import dataclass
import random

if TYPE_CHECKING:
    from src.classes.avatar import Avatar
    from src.classes.world import World

@dataclass
class ChatMessage:
    sender_id: str
    receiver_id: str
    content: str
    timestamp: int
    is_read: bool = False

from enum import Enum
import uuid

class EncounterType(Enum):
    NORMAL = "normal"       # 普通路人
    ELITE = "elite"         # 精英/男神女神
    TRAP = "trap"           # 陷阱

class TrapType(Enum):
    NONE = "none"
    CATFISH = "catfish"     # 照骗
    SCAMMER = "scammer"     # 杀猪盘
    MOOCHER = "moocher"     # 酒托/饭托

@dataclass
class SocialEncounter:
    id: str
    type: EncounterType
    name: str
    age: int
    occupation: str
    tags: List[str]
    
    # Displayed stats (what the player sees)
    display_appearance: int
    display_wealth: int
    
    # Real stats (hidden)
    real_appearance: int
    real_wealth: int
    trap_type: TrapType = TrapType.NONE
    
    # Interaction state
    is_matched: bool = False
    
class SocialAppManager:
    """
    Manages the 'Dungeon' of modern romance: Social Apps (Tinder/Soul etc).
    """
    def __init__(self, world: "World"):
        self.world = world
        self.current_encounters: Dict[str, SocialEncounter] = {} # temporary storage for current session swipes

    def swipe(self, player: "Avatar") -> Optional[SocialEncounter]:
        """
        Consume energy to find a new match.
        Returns an Encounter object.
        """
        # 1. Check Energy
        player.ensure_modern_profile()
        if player.modern_profile.energy < 15:
            return None # Not enough energy
            
        player.update_modern_status(energy_delta=-15)
        
        # 2. Determine Encounter Type based on probabilities
        # Base: Normal 60%, Elite 10%, Trap 30%
        
        roll = random.random()
        encounter_type = EncounterType.NORMAL
        trap_type = TrapType.NONE
        
        trap_chance = 0.3
        elite_chance = 0.1
        
        # Modifiers
        # Rich players attract more scammers and elites
        if player.modern_profile.assets > 100000:
            trap_chance += 0.2
        if player.modern_profile.assets > 1000000:
            trap_chance += 0.1
            elite_chance += 0.1
            
        # High status players attract more elites but also traps
        if player.modern_profile.social_status > 80:
            elite_chance += 0.1
            trap_chance += 0.1
            
        # Normalize if chances exceed 1.0 (unlikely but safe)
        total_special = trap_chance + elite_chance
        if total_special > 0.9:
            scale = 0.9 / total_special
            trap_chance *= scale
            elite_chance *= scale
            
        if roll < elite_chance:
            encounter_type = EncounterType.ELITE
        elif roll < elite_chance + trap_chance:
            encounter_type = EncounterType.TRAP
            # Determine trap type
            trap_roll = random.random()
            if trap_roll < 0.4:
                trap_type = TrapType.CATFISH
            elif trap_roll < 0.8:
                trap_type = TrapType.SCAMMER
            else:
                trap_type = TrapType.MOOCHER
        
        # 3. Generate Profile Data
        encounter = self._generate_encounter(encounter_type, trap_type)
        self.current_encounters[encounter.id] = encounter
        
        return encounter

    def _generate_encounter(self, etype: EncounterType, ttype: TrapType) -> SocialEncounter:
        """Generate random encounter data."""
        # Simple random generation for now
        # Ideally this should come from a name/job database
        
        fake_id = str(uuid.uuid4())
        
        # Defaults for Normal
        display_app = random.randint(50, 80)
        display_wealth = random.randint(30, 70)
        real_app = display_app
        real_wealth = display_wealth
        name = "Passerby " + fake_id[:4]
        occupation = "Employee"
        tags = ["Travel", "Foodie"]
        
        if etype == EncounterType.ELITE:
            display_app = random.randint(85, 99)
            display_wealth = random.randint(80, 99)
            real_app = display_app
            real_wealth = display_wealth
            name = "Elite " + fake_id[:4]
            occupation = "Executive"
            tags = ["Golf", "Investment", "Art"]
            
        elif etype == EncounterType.TRAP:
            name = "Stranger " + fake_id[:4]
            if ttype == TrapType.CATFISH:
                display_app = random.randint(90, 99) # Looks hot
                real_app = random.randint(30, 50)    # Actually not
                tags = ["Model", "Fitness"]
            elif ttype == TrapType.SCAMMER:
                display_wealth = random.randint(90, 99) # Looks rich
                real_wealth = 0
                occupation = "Crypto Investor"
                tags = ["Finance", "Crypto"]
            elif ttype == TrapType.MOOCHER:
                display_app = random.randint(80, 90)
                display_wealth = random.randint(40, 60)
                tags = ["Party", "Wine"]
                
        return SocialEncounter(
            id=fake_id,
            type=etype,
            name=name,
            age=random.randint(20, 35),
            occupation=occupation,
            tags=tags,
            display_appearance=display_app,
            display_wealth=display_wealth,
            real_appearance=real_app,
            real_wealth=real_wealth,
            trap_type=ttype
        )

    def ice_break(self, player: "Avatar", encounter_id: str, choice_type: str) -> bool:
        """
        Attempt to break the ice.
        choice_type: 'HUMOR', 'SINCERE', 'PICKUP_LINE'
        Returns True if success (added to contacts), False otherwise.
        """
        if encounter_id not in self.current_encounters:
            return False
            
        encounter = self.current_encounters[encounter_id]
        
        # Simple logic: 
        # Elite is hard to get.
        # Trap is easy to get (they want to trap you).
        # Normal depends on match.
        
        success_chance = 0.5
        
        if encounter.type == EncounterType.TRAP:
            success_chance = 0.9 # Traps are eager
        elif encounter.type == EncounterType.ELITE:
            success_chance = 0.2 # Elites are picky
            # Modifiers based on player stats could go here
            if player.modern_profile.assets > 80: # Rich player
                success_chance += 0.3
            if player.modern_profile.social_status > 80:
                success_chance += 0.3
                
        # Choice modifiers (mock)
        if choice_type == "HUMOR":
            success_chance += 0.1
        elif choice_type == "PICKUP_LINE":
            success_chance -= 0.1 # Risky
            
        is_success = random.random() < success_chance
        
        if is_success:
            # Create a lightweight contact entry
            # In a full implementation, this would be a real Avatar
            player.ensure_modern_profile()
            
            contact_data = {
                "affection": 15, # Starts as Acquaintance
                "name": encounter.name,
                "occupation": encounter.occupation,
                "age": encounter.age,
                "tags": encounter.tags,
                "is_npc": False, # Lightweight contact
                "encounter_id": encounter.id,
                "type": encounter.type.value,
                "trap_type": encounter.trap_type.value
            }
            
            player.modern_profile.relationships[encounter.id] = contact_data
            
        return is_success

class ChatManager:
    """
    Manages chat interactions between avatars.
    """
    def __init__(self, world: "World"):
        self.world = world
        self.history: List[ChatMessage] = []

    def generate_reply(self, sender: "Avatar", receiver: "Avatar", content: str) -> str:
        """
        Generates a reply using LLM (mocked for now).
        """
        # TODO: Integrate LLM here
        # Context: Relationship stage, mood, personality, past history
        
        replies = [
            "哈哈，真的吗？",
            "我也这么觉得！",
            "有点忙，晚点聊。",
            "...",
            f"你对 {content} 怎么看？"
        ]
        return random.choice(replies)

    def send_message(self, sender: "Avatar", receiver: "Avatar", content: str) -> ChatMessage:
        """
        Sends a message from sender to receiver.
        """
        msg = ChatMessage(
            sender_id=sender.id,
            receiver_id=receiver.id,
            content=content,
            timestamp=int(self.world.month_stamp)
        )
        self.history.append(msg)
        
        # Update Relationship (Small interaction)
        if hasattr(sender, "update_modern_status"):
             # Sender spends energy
             sender.update_modern_status(energy_delta=-2)
             
        # Receiver logic (maybe async reply?)
        return msg

class DateManager:
    """
    Manages dating interactions.
    """
    def __init__(self, world: "World"):
        self.world = world

    def propose_date(self, initiator: "Avatar", target: "Avatar", location: str) -> bool:
        """
        Propose a date. Returns success/fail.
        """
        # Logic: Check affection, mood, schedule availability
        if not hasattr(initiator, "get_relationship_stage"):
            return False
            
        stage = initiator.get_relationship_stage(target)
        
        base_chance = 0.5
        if stage.value >= 2: # Friend
            base_chance += 0.3
            
        if target.modern_profile and target.modern_profile.mood > 60:
            base_chance += 0.2
            
        return random.random() < base_chance

    def start_date(self, initiator: "Avatar", target: "Avatar", location: str) -> str:
        """
        Start the date event.
        """
        # 1. Define location costs and benefits
        location_config = {
            "park": {"cost": 0, "energy": 10, "mood_bonus": 5, "stress_relief": 10},
            "cafe": {"cost": 100, "energy": 5, "mood_bonus": 10, "stress_relief": 5},
            "restaurant": {"cost": 500, "energy": 15, "mood_bonus": 15, "stress_relief": 5},
            "movie": {"cost": 200, "energy": 5, "mood_bonus": 10, "stress_relief": 15},
            "bar": {"cost": 300, "energy": 20, "mood_bonus": 5, "stress_relief": 5},
            "hotel": {"cost": 1000, "energy": 30, "mood_bonus": 20, "stress_relief": 20}
        }
        
        config = location_config.get(location, location_config["park"])
        
        # 2. Check Resources
        if hasattr(initiator, "ensure_modern_profile"):
            initiator.ensure_modern_profile()
            
        mp = initiator.modern_profile
        if mp.assets < config["cost"]:
            return f"资金不足，无法在 {location} 约会。"
        if mp.energy < config["energy"]:
            return f"精力不足，无法进行约会。"
            
        # 3. Consume Resources
        mp.assets -= config["cost"]
        initiator.update_modern_status(energy_delta=-config["energy"])
        
        # 4. Calculate Outcome
        # Base affection gain
        affection_gain = 5
        
        # Mood bonus
        if target.modern_profile:
            if target.modern_profile.mood > 70:
                affection_gain += 3
            elif target.modern_profile.mood < 30:
                affection_gain -= 2
                
        # 5. Apply Effects
        # Update Initiator
        initiator.update_modern_status(mood_delta=config["mood_bonus"], stress_delta=-config["stress_relief"])
        
        # Update Target
        if hasattr(target, "update_modern_status"):
            target.update_modern_status(mood_delta=config["mood_bonus"], stress_delta=-config["stress_relief"])
            
        # Update Relationship
        # We need a way to update affection. 
        # The Mixin has 'get_relationship_stage' but not 'update_relationship'.
        # Assuming there is a standard way or we modify the dictionary directly for now.
        if hasattr(initiator, "relations"):
             # Use the standard relation system if available, or the modern profile dict
             # Let's check if 'relations' attribute exists on Avatar (it should)
             pass 
             
        # For now, update the modern profile relationships dict directly as fallback or primary
        target.ensure_modern_profile()
        
        # Initiator -> Target
        if target.id not in mp.relationships:
            mp.relationships[target.id] = {"affection": 0}
        mp.relationships[target.id]["affection"] += affection_gain
        
        # Target -> Initiator
        tmp = target.modern_profile
        if initiator.id not in tmp.relationships:
            tmp.relationships[initiator.id] = {"affection": 0}
        tmp.relationships[initiator.id]["affection"] += affection_gain

        return f"在 {location} 的约会很愉快！好感度 +{affection_gain}，花费 {config['cost']}，心情提升。"
