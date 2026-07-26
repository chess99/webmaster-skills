import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "skills" / "find-product-opportunities" / "scripts"
sys.path.insert(0, str(SCRIPTS))
