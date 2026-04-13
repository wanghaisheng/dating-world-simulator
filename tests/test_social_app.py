print("Starting test_social_app.py...")
import sys
import os
from pathlib import Path

# Force add project root to path
sys.path.append("E:\\workspace\\cultivation-world-simulator")
print(f"Path added. Current path: {sys.path}")

try:
    from src.classes.modern.social_system import SocialAppManager, EncounterType, TrapType
    print("Import successful.")
except ImportError as e:
    print(f"Import failed: {e}")
    sys.exit(1)

from dataclasses import dataclass, field
from typing import Optional, Dict, List
import random

# Mock classes to avoid heavy dependencies
@dataclass
class ModernProfile:
    energy: int = 100
    assets: int = 0
    social_status: int = 0
    relationships: Dict[str, dict] = field(default_factory=dict)
    
class MockAvatar:
    def __init__(self):
        self.modern_profile = ModernProfile()
        self.id = "mock_player"
        
    def ensure_modern_profile(self):
        pass
        
    def update_modern_status(self, energy_delta=0, **kwargs):
        self.modern_profile.energy += energy_delta

class MockWorld:
    def __init__(self):
        self.month_stamp = 0

def test_social_app():
    print("Testing Social App Manager...")
    
    world = MockWorld()
    manager = SocialAppManager(world)
    
    # Create a mock player
    player = MockAvatar()
    player.modern_profile.energy = 100
    player.modern_profile.assets = 50000
    
    print(f"Initial Energy: {player.modern_profile.energy}")
    
    # Test Swipe
    print("\n--- Testing Swipe ---")
    encounter = manager.swipe(player)
    
    if encounter:
        print(f"Swipe Result: {encounter.type.name} - {encounter.name}")
        print(f"Stats: App={encounter.display_appearance}, Wealth={encounter.display_wealth}")
        print(f"Trap Type: {encounter.trap_type.name}")
        print(f"Remaining Energy: {player.modern_profile.energy}")
        
        # Test Ice Break
        print("\n--- Testing Ice Break ---")
        random.seed(42) 
        
        success = manager.ice_break(player, encounter.id, "SINCERE")
        print(f"Ice Break (SINCERE) Result: {'Success' if success else 'Fail'}")
        
        if success:
            print(f"Contact Added: {encounter.id in player.modern_profile.relationships}")
            if encounter.id in player.modern_profile.relationships:
                contact = player.modern_profile.relationships[encounter.id]
                print(f"Contact Name: {contact['name']}")
                print(f"Affection: {contact['affection']}")
        
    else:
        print("Swipe failed (not enough energy?)")
        
    # Test Trap Logic (Rich Player)
    print("\n--- Testing Trap Logic (Rich Player) ---")
    player.modern_profile.assets = 1000000 # Very rich
    player.modern_profile.energy = 1000 # Infinite energy
    
    traps_found = 0
    elites_found = 0
    
    for i in range(20):
        enc = manager.swipe(player)
        if enc:
            if enc.type == EncounterType.TRAP:
                traps_found += 1
            elif enc.type == EncounterType.ELITE:
                elites_found += 1
            
    print(f"Traps found in 20 swipes (Rich): {traps_found}")
    print(f"Elites found in 20 swipes (Rich): {elites_found}")

if __name__ == "__main__":
    test_social_app()
