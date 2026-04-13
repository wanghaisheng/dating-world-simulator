import sys
import os
sys.path.append(os.getcwd())

from src.classes.avatar.core import Avatar, Gender
from src.classes.age import Age
from src.classes.cultivation import CultivationProgress
from src.classes.world import World
from src.classes.calendar import MonthStamp
from src.utils.config import CONFIG, GameMode

def test_modern_profile_initialization():
    # Force game mode to MODERN_ROMANCE
    # CONFIG.game is an OmegaConf object (DictConfig)
    # We can assign to it
    from omegaconf import OmegaConf
    if not hasattr(CONFIG, "game"):
        CONFIG.game = OmegaConf.create({})
    CONFIG.game.mode = "modern_romance"
    
    # Mock World
    class MockWorld:
        pass
    world = MockWorld()
    
    # Create Avatar
    # Note: Avatar dataclass fields: world, name, id, birth_month_stamp, age, gender are required.
    avatar = Avatar(
        world=world,
        name="TestUser",
        id="123",
        birth_month_stamp=MonthStamp(0),
        age=Age(20, None),
        gender=Gender.MALE
    )
    
    # Check if modern_profile is initialized
    if avatar.modern_profile is not None:
        print("SUCCESS: modern_profile is initialized.")
        print(f"Occupation: {avatar.modern_profile.occupation}")
        
        # Test serialization
        from src.sim.save.avatar_save_mixin import AvatarSaveMixin
        # Avatar inherits AvatarSaveMixin
        save_dict = avatar.to_save_dict()
        if "modern_profile" in save_dict and save_dict["modern_profile"] is not None:
            print("SUCCESS: modern_profile is serialized.")
        else:
            print("FAILURE: modern_profile is NOT serialized.")
            
        # Test deserialization
        # We need to mock a bit more for from_save_dict to work, or just test the specific part manually
        # But let's try calling from_save_dict if possible, but it has many dependencies (from src.classes...)
        # Might be hard to mock everything.
        
    else:
        print("FAILURE: modern_profile is None.")

def test_relationship_stages():
    from src.classes.avatar.modern_mixin import RelationshipStage
    
    # Setup mocks
    class MockWorld: pass
    world = MockWorld()
    
    # Create Avatars
    # Note: Avatar constructor requires specific types for some fields
    avatar = Avatar(world=world, name="MC", id="mc", birth_month_stamp=MonthStamp(0), age=Age(20, None), gender=Gender.MALE)
    partner = Avatar(world=world, name="Partner", id="p1", birth_month_stamp=MonthStamp(0), age=Age(20, None), gender=Gender.FEMALE)
    
    # Init profile
    avatar.ensure_modern_profile()
    
    # Test Stranger (default 0)
    stage = avatar.get_relationship_stage(partner)
    if stage == RelationshipStage.STRANGER:
        print("SUCCESS: Stranger stage verified.")
    else:
        print(f"FAILURE: Expected STRANGER, got {stage}")
    
    # Test Acquaintance (20)
    avatar.modern_profile.relationships[partner.id] = {"affection": 20}
    stage = avatar.get_relationship_stage(partner)
    if stage == RelationshipStage.ACQUAINTANCE:
        print("SUCCESS: Acquaintance stage verified.")
    else:
        print(f"FAILURE: Expected ACQUAINTANCE, got {stage}")
    
    # Test Friend (50)
    avatar.modern_profile.relationships[partner.id] = {"affection": 50}
    stage = avatar.get_relationship_stage(partner)
    if stage == RelationshipStage.FRIEND:
        print("SUCCESS: Friend stage verified.")
    else:
        print(f"FAILURE: Expected FRIEND, got {stage}")
    
    # Test Crush (70)
    avatar.modern_profile.relationships[partner.id] = {"affection": 70}
    stage = avatar.get_relationship_stage(partner)
    if stage == RelationshipStage.CRUSH:
        print("SUCCESS: Crush stage verified.")
    else:
        print(f"FAILURE: Expected CRUSH, got {stage}")
    
    # Test Lover (90)
    avatar.modern_profile.relationships[partner.id] = {"affection": 90}
    stage = avatar.get_relationship_stage(partner)
    if stage == RelationshipStage.LOVER:
        print("SUCCESS: Lover stage verified.")
    else:
        print(f"FAILURE: Expected LOVER, got {stage}")

if __name__ == "__main__":
    test_modern_profile_initialization()
    test_relationship_stages()
