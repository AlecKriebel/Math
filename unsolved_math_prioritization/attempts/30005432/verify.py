from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).resolve().parent/"publication_package"/'verify.py'),run_name="__main__")
