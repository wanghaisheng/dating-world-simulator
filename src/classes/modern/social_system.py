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
