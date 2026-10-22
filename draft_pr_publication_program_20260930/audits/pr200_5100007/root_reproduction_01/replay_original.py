from pathlib import Path
import sys,runpy
root=Path(__file__).resolve().parent
sys.path.insert(0,str(root.parent/'math_algebra_family_01/runtime_packages'))
runpy.run_path(str(root/sys.argv[1]/'verify.py'),run_name='__main__')
