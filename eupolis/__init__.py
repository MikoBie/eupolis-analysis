__all__ = ["utils"]
from pathlib import Path

ROOT = Path(__file__).absolute().parent.parent
DATA = ROOT / "data"
RAW = DATA / "raw"
PROC = DATA / "processed"
PNG = ROOT / "png"
