from __future__ import annotations

import sys
from pathlib import Path


if __package__:
    from .cli import main
else:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from opportunity_radar.cli import main


raise SystemExit(main())
