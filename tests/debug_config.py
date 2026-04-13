import sys
import os
sys.path.append(os.getcwd())
from src.utils.config import CONFIG

print("CONFIG loaded")
print(f"CONFIG keys: {CONFIG.keys()}")
if hasattr(CONFIG, "avatar"):
    print(f"CONFIG.avatar: {CONFIG.avatar}")
else:
    print("CONFIG.avatar is MISSING")
