import sys
import os
sys.path.append(os.getcwd())

try:
    print("Attempting to import src.classes.avatar.core...")
    from src.classes.avatar.core import Avatar
    print("Import successful!")
except Exception as e:
    print(f"Import failed: {e}")
    import traceback
    traceback.print_exc()
