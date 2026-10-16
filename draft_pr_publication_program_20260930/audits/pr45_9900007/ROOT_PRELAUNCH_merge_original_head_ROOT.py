"""ROOT's exact preflight-guarded original-head merge; preserve actual conflicts."""
from pathlib import Path
import os, subprocess, sys
A=Path(__file__).resolve().parent;R=A.parents[2]
sys.path.insert(0,str(A/'acceptance_preparation_family'));sys.dont_write_bytecode=True
import pr45_guards as g
def main():
    assert __debug__
    pre=g.load(A/'integration_preflight.json')
    assert g.git('branch','--show-current')=='main'and g.git('rev-parse','HEAD')==pre['main_before']
    assert not g.git('diff','--cached','--name-only')
    g.fresh_check(pre)
    return subprocess.call(['git','merge','--no-ff','--no-commit',g.HEAD],cwd=R,stdin=subprocess.DEVNULL)
if __name__=='__main__':sys.exit(main())
