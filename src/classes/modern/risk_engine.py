import random
from typing import TYPE_CHECKING, Optional, Tuple, List

if TYPE_CHECKING:
    from src.classes.avatar.core import Avatar

class RelationshipRiskEngine:
    """
    Engine for handling high-risk relationship dynamics in Modern Romance mode.
    Handles exploitation, manipulation, scams, and infidelity.
    """

    @staticmethod
    def check_daily_risks(avatar: "Avatar", partners: List["Avatar"]) -> List[str]:
        """
        Check for any risk events that might trigger today with current partners.
        Returns a list of event descriptions (for logging/notification).
        """
        events = []
        
        # 1. Check for Harem/Conflict Risks (Multi-dating overlap)
        conflict_event = RelationshipRiskEngine._check_harem_conflict(avatar, partners)
        if conflict_event:
            events.append(conflict_event)

        # 2. Check Individual Partner Risks
        for partner in partners:
            if not partner.modern_profile:
                continue
            
            # Skip if partner is sincere (sincerity > 60) and has no negative archetype
            # Unless we want some false positives or misunderstandings? For now, keep it simple.
            if partner.modern_profile.sincerity > 60 and not partner.modern_profile.hidden_archetype:
                continue

            event = RelationshipRiskEngine.evaluate_partner_risk(avatar, partner)
            if event:
                events.append(event)
        
        return events

    @staticmethod
    def _check_harem_conflict(avatar: "Avatar", partners: List["Avatar"]) -> Optional[str]:
        """Check for conflicts arising from multi-dating in danger zones."""
        from src.classes.avatar.modern_mixin import RelationshipStage
        
        danger_zone_partners = []
        for p in partners:
            if not p.modern_profile: continue
            # We assume 'avatar' has the mixin if we are here, but let's be safe
            if not hasattr(avatar, 'get_relationship_stage'):
                continue
                
            stage = avatar.get_relationship_stage(p)
            # Danger Zone: CRUSH (Ambiguous) or higher
            if stage.value >= RelationshipStage.CRUSH.value:
                danger_zone_partners.append(p)
                
        if len(danger_zone_partners) < 2:
            return None
            
        # Conflict Risk!
        # Base chance 10% per day per extra partner
        # Reduced by Avatar's Intelligence or Luck (TODO)
        risk_chance = 0.1 * (len(danger_zone_partners) - 1)
        
        if random.random() < risk_chance:
            # Trigger Conflict
            names = ", ".join([p.name for p in danger_zone_partners])
            # Penalties: High Stress, Low Mood
            if hasattr(avatar, 'update_modern_status'):
                avatar.update_modern_status(stress_delta=20, mood_delta=-20)
                
            return f"【修罗场爆发】你同时与 {len(danger_zone_partners)} 位处于暧昧/恋爱阶段的异性 ({names}) 纠缠不清的事情败露了！心情 -20, 压力 +20。"
            
        return None

    @staticmethod
    def evaluate_partner_risk(avatar: "Avatar", partner: "Avatar") -> Optional[str]:
        """Evaluate risk for a specific partner."""
        archetype = partner.modern_profile.hidden_archetype
        if not archetype:
            return None
        
        # Risk probability increases with lower sincerity and higher dependency/affection
        # But some archetypes wait for high affection to strike (pig butchering scam)
        
        base_chance = 0.05 # 5% daily chance of something happening if conditions met
        
        if archetype == "GOLD_DIGGER":
            return RelationshipRiskEngine._handle_gold_digger(avatar, partner, base_chance)
        elif archetype == "NPD":
            return RelationshipRiskEngine._handle_npd(avatar, partner, base_chance)
        elif archetype == "SCAMMER":
            return RelationshipRiskEngine._handle_scammer(avatar, partner, base_chance)
        elif archetype == "PUA":
            return RelationshipRiskEngine._handle_pua(avatar, partner, base_chance)
        elif archetype == "PLAYER":
            return RelationshipRiskEngine._handle_player(avatar, partner, base_chance)
            
        return None

    @staticmethod
    def _handle_gold_digger(avatar: "Avatar", partner: "Avatar", chance: float) -> Optional[str]:
        if random.random() > chance:
            return None
        
        # Logic: Ask for expensive gift
        cost = random.randint(1000, 10000)
        
        # If avatar is rich, they might just pay to keep partner happy
        if avatar.modern_profile and avatar.modern_profile.assets >= cost:
            # 50% chance to succumb to pressure
            if random.random() < 0.5:
                avatar.modern_profile.assets -= cost
                avatar.update_modern_status(stress_delta=5) # Paying relieves immediate pressure but adds stress?
                return f"{partner.name} (捞女) 暗示想要一个价值 {cost} 的礼物。你为了讨好她买下了礼物 (金钱 -{cost})。"
            else:
                # Refuse
                avatar.update_modern_status(mood_delta=-5)
                return f"{partner.name} (捞女) 想要价值 {cost} 的礼物，但你拒绝了。她看起来很不高兴 (心情 -5)。"
        else:
            avatar.update_modern_status(mood_delta=-10, stress_delta=5)
            return f"{partner.name} (捞女) 嫌弃你太穷，买不起 {cost} 的礼物，没有给你好脸色看 (心情 -10)。"

    @staticmethod
    def _handle_npd(avatar: "Avatar", partner: "Avatar", chance: float) -> Optional[str]:
        # NPD strikes when relationship is established (affection > 50)
        # We need a way to check affection. Assuming standard way or mixin helper.
        # For now, relying on chance mostly as 'check_daily_risks' filters somewhat.
            
        if random.random() > chance:
            return None
            
        # Gaslighting / Devaluation
        if avatar.modern_profile:
            # Significant mental damage
            avatar.update_modern_status(mood_delta=-15, stress_delta=10)
            
            # Potential isolation (reduce relationship with others?) - too complex for now
            
        return f"{partner.name} (NPD) 对你进行了一番打压，贬低你的成就，让你觉得自己一无是处 (心情 -15, 压力 +10)。"

    @staticmethod
    def _handle_scammer(avatar: "Avatar", partner: "Avatar", chance: float) -> Optional[str]:
        # Scammer waits for high trust
        # We assume evaluate_partner_risk calls this only if appropriate
            
        # Low chance but high impact
        if random.random() > (chance * 0.5):
            return None
            
        if avatar.modern_profile and avatar.modern_profile.assets > 5000:
            loss = int(avatar.modern_profile.assets * 0.8) # Lose 80% of assets!
            avatar.modern_profile.assets -= loss
            avatar.update_modern_status(stress_delta=50, mood_delta=-50)
            return f"【重大危机】{partner.name} (杀猪盘) 推荐的'理财产品'暴雷了！你损失了 {loss} 资金 (资产 -80%)，心情崩溃 (心情 -50, 压力 +50)。"
            
        return f"{partner.name} (杀猪盘) 试图忽悠你投资，但你没钱，逃过一劫。"

    @staticmethod
    def _handle_pua(avatar: "Avatar", partner: "Avatar", chance: float) -> Optional[str]:
         if random.random() > chance:
            return None
            
         if avatar.modern_profile:
             avatar.update_modern_status(mood_delta=-5, energy_delta=-10)
            
         return f"{partner.name} (PUA) 对你使用了冷读术和忽冷忽热的技巧，让你患得患失 (心情 -5, 精力 -10)。"

    @staticmethod
    def _handle_player(avatar: "Avatar", partner: "Avatar", chance: float) -> Optional[str]:
        if random.random() > chance:
            return None
            
        # Discovery event
        if avatar.modern_profile:
             avatar.update_modern_status(stress_delta=10)
             
        return f"你偶然发现 {partner.name} (海王) 的手机上弹出了一条暧昧消息，对方似乎不仅只有你一个伴侣 (压力 +10)。"
