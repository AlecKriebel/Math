from pathlib import Path
import sys
Path(sys.argv[2]).write_text("must be blocked\n")
