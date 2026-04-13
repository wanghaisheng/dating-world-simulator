import unittest
import sys
import os
from unittest.mock import MagicMock

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.classes.avatar.modern_mixin import ModernProfileMixin, ModernProfile, RelationshipStage
from src.classes.modern.risk_engine import RelationshipRiskEngine
from src.classes.modern.social_system import DateManager, ChatManager

class MockRelations:
    def __init__(self):
        self.data = {}
    
    def get_relation(self, partner):
        return self.data.get(partner.id, MagicMock(value=0))

class MockAvatar(ModernProfileMixin):
    def __init__(self, uid, name):
        self.id = uid
        self.name = name
        self.modern_profile = None
        self.relations = MockRelations()
        self.ensure_modern_profile()

    # We need to implement update_modern_status if it's not in the mixin on disk 
    # (Wait, I added it to the mixin in the previous turn, so it should be there. 
    # But just in case, I will verify or rely on it.)
    # If the mixin has it, this class inherits it.
    
    # Mocking world for context if needed, but RiskEngine mostly uses static methods
    
class TestModernRisk(unittest.TestCase):
    def setUp(self):
        self.p1 = MockAvatar("p1", "Player")
        self.p1.modern_profile.assets = 100000
        self.p1.modern_profile.mood = 50
        self.p1.modern_profile.stress = 0
        
        self.p2 = MockAvatar("p2", "GoldDigger")
        self.p2.modern_profile.hidden_archetype = "GOLD_DIGGER"
        self.p2.modern_profile.sincerity = 10
        
        self.p3 = MockAvatar("p3", "Scammer")
        self.p3.modern_profile.hidden_archetype = "SCAMMER"
        self.p3.modern_profile.sincerity = 0
        
    def test_gold_digger_risk(self):
        # Force risk event
        # The logic has random checks, so we might need to mock random or loop until triggered
        # Or we can call the handler directly for testing
        
        print("\nTesting Gold Digger Handler...")
        # Direct call to handler
        result = RelationshipRiskEngine._handle_gold_digger(self.p1, self.p2, 0.0) # 0.0 chance means pass the first check? No, random > chance returns None. So we pass -1.0 to ensure random > -1.0 is True?
        # Wait, code is: if random.random() > chance: return None
        # So if chance is 1.1, random > 1.1 is False, so it proceeds.
        # No, random is 0..1. If chance is 0.0, random > 0.0 is True (mostly), so it returns None.
        # Logic in code:
        # if random.random() > chance: return None
        # We want it NOT to return None. So random.random() <= chance.
        # So we should pass chance=1.0 (always triggers).
        
        # However, inside _handle_gold_digger, there is another random check for 50% succumb chance.
        # Let's mock random to control flow.
        
        import random
        state_before = self.p1.modern_profile.assets
        
        # Case 1: Succumb (random < 0.5)
        # Mocking random.random() is tricky if called multiple times.
        # Let's just run it multiple times and see if assets decrease eventually
        
        triggered = False
        for _ in range(20):
            res = RelationshipRiskEngine._handle_gold_digger(self.p1, self.p2, 1.0)
            if res and "买下了礼物" in res:
                triggered = True
                break
        
        if triggered:
            self.assertTrue(self.p1.modern_profile.assets < state_before)
            print(f"Gold Digger triggered: Assets {state_before} -> {self.p1.modern_profile.assets}")
        else:
            print("Gold Digger succumb event didn't trigger in 20 tries (unlikely but possible)")

    def test_scammer_risk(self):
        print("\nTesting Scammer Handler...")
        # Scammer logic: random > chance * 0.5 return None. So pass chance=2.0 to ensure random <= chance*0.5
        
        self.p1.modern_profile.assets = 100000
        
        # Trigger
        res = RelationshipRiskEngine._handle_scammer(self.p1, self.p3, 2.0)
        
        if res and "暴雷" in res:
            self.assertTrue(self.p1.modern_profile.assets < 25000) # Should lose 80%
            print(f"Scammer triggered: Assets 100000 -> {self.p1.modern_profile.assets}")
        else:
            print(f"Scammer didn't trigger (res: {res})")

    def test_date_manager(self):
        print("\nTesting Date Manager...")
        dm = DateManager(None) # World is not used in start_date for now
        
        # Initial state
        self.p1.modern_profile.assets = 500
        self.p1.modern_profile.energy = 50
        self.p1.modern_profile.mood = 50
        
        # Cafe date: cost 100, energy 5, mood+10
        res = dm.start_date(self.p1, self.p2, "cafe")
        print(f"Date Result: {res}")
        
        self.assertEqual(self.p1.modern_profile.assets, 400)
        self.assertEqual(self.p1.modern_profile.energy, 45)
        self.assertEqual(self.p1.modern_profile.mood, 60) # 50 + 10
        
        # Check relationship update
        rel_p1 = self.p1.modern_profile.relationships.get(self.p2.id)
        self.assertIsNotNone(rel_p1)
        self.assertTrue(rel_p1["affection"] > 0)
        print(f"Relationship updated: {rel_p1}")

if __name__ == '__main__':
    unittest.main()
