#!/usr/bin/env python3
"""Run the unchanged frozen reviewer code with a relocated author-packet path.
Only its one literal input-directory assignment is rebound in memory.
"""
from pathlib import Path
import sys
here=Path(__file__).resolve().parent
packet=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else here.parent
source=(here/'independent_checks.py').read_text()
old="Path('/workspace/shared/math-30004033-final')"
assert source.count(old)==1, 'Unexpected frozen checker input-path expression'
source=source.replace(old,'Path('+repr(str(packet))+')')
exec(compile(source,str(here/'independent_checks.py'),'exec'),{'__name__':'__main__'})
