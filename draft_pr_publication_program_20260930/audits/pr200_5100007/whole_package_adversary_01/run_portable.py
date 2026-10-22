from pathlib import Path
import sys, runpy
runtime=Path(__file__).resolve().parent.parent/'math_algebra_family_01'/'runtime_packages'
sys.path.insert(0,str(runtime))
script=Path(sys.argv[1]).resolve()
sys.argv=sys.argv[1:]
runpy.run_path(str(script),run_name='__main__')
