import sys
from pathlib import Path

# Add "app"  directory to the path
sys.path.append(str(Path(__file__).parent.parent) + "app")
print(sys.path)