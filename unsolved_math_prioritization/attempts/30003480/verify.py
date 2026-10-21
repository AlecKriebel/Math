"""Run the active exact standard-library controls beside this native package."""
from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).resolve().parent/"publication_package"/"verify_exact.py"),run_name="__main__")
