import asyncio
import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils.config import CONFIG, GameMode
from src.classes.world import World
from src.sim.simulator import Simulator
from src.classes.calendar import create_month_stamp, Year, Month
from src.sim.new_avatar import make_avatars

async def test_modern_loop():
    print(f"Current Game Mode: {CONFIG.game.mode}")
    
    # Verify mode
    if CONFIG.game.mode != GameMode.MODERN_ROMANCE.value:
        print("Error: Game mode is not modern_romance")
        return

    # Create World
    world = World()
    world.init_world(create_month_stamp(Year(2025), Month.JANUARY))
    
    # Create Avatars
    # make_avatars logic might need adjustment for modern mode (no sects, etc.)
    # But for now, let's see if it works with defaults or if we need to manually create avatars
    avatars = make_avatars(world, count=5)
    
    print(f"Created {len(avatars)} avatars.")
    
    # Check Modern Profile
    first_avatar = list(avatars.values())[0]
    first_avatar.ensure_modern_profile()
    print(f"Avatar {first_avatar.name} occupation: {first_avatar.get_modern_occupation()}")
    
    # Initialize Simulator
    sim = Simulator(world)
    
    # Run loop for 24 hours (24 ticks)
    print("Starting simulation...")
    for i in range(25):
        hour = int(world.month_stamp) % 24
        print(f"Tick {i}, Hour: {hour}")
        
        await sim.step()
        
        # Check status of first avatar
        if hasattr(first_avatar, "modern_profile") and first_avatar.modern_profile:
            p = first_avatar.modern_profile
            sched = first_avatar.get_scheduled_activity(hour)
            print(f"  {first_avatar.name}: Energy={p.energy}, Stress={p.stress}, Activity={sched}")
            
    print("Simulation finished.")

if __name__ == "__main__":
    asyncio.run(test_modern_loop())
