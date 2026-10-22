"""Replay an archived original without modifying any original file.

__file__ is redirected into this audit folder solely to redirect the reviewer's
receipt output. Source code is compiled verbatim with its actual original path.
"""
import sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]/'pr200_5100007'/'math_algebra_family_01'/'runtime_packages'))
choice=sys.argv[1]
paths={'exact':'turn1_exact.py','generic':'turn1_generic_six.py','reviewer':'independent_review/independent_check.py'}
if choice not in paths:raise RuntimeError('unknown replay script')
src=HERE.parent/'original_submitted_head'/paths[choice]
dest=HERE/'original_replays'/('optimized' if sys.flags.optimize else 'normal')/choice
dest.mkdir(parents=True,exist_ok=True)
ns={'__name__':'__main__','__file__':str(dest/src.name),'__builtins__':__builtins__}
exec(compile(src.read_text(),str(src),'exec'),ns)
