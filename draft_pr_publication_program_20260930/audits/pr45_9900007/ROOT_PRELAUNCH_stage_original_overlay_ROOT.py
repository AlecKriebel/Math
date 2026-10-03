"""Stage only the exact505 reviewed overlay bodies and the one accepted queue."""
from pathlib import Path
import json,subprocess,sys
A=Path(__file__).resolve().parent;R=A.parents[2];sys.dont_write_bytecode=True
sys.path.insert(0,str(A/'acceptance_preparation_family'));import pr45_guards as g
def main():
    assert __debug__
    pre=g.load(A/'integration_preflight.json');overlay=g.load(A/'integration_check.json')
    assert g.git('rev-parse','HEAD')==pre['main_before']and g.git('rev-parse','MERGE_HEAD')==g.HEAD
    rr=overlay['canonical_overlay_files'];assert len(rr)==505
    g.check(g.K,rr);g.fresh_check(pre,{'unsolved_math_prioritization/QUEUE.md'})
    prefix=g.K.relative_to(R).as_posix()+'/'
    names={prefix+z['path']for z in rr}|{'unsolved_math_prioritization/QUEUE.md'}
    staged=set(g.git_bytes('diff','--cached','--name-only','-z').decode().split('\0'))-{''}
    assert staged<=names,staged-names
    subprocess.run(['git','add','-f','--',*sorted(names)],cwd=R,check=True)
    assert not g.git('diff','--name-only','--diff-filter=U')
    actual=set(g.git_bytes('diff','--cached','--name-only','-z').decode().split('\0'))-{''}
    assert actual==names
    for z in rr:
        n=prefix+z['path'];raw=g.git_bytes('show',':'+n)
        assert len(raw)==z['bytes']and g.sha(raw)==z['sha256']
        e=g.git_bytes('ls-files','--stage','-z','--',n).decode().rstrip('\0')
        assert e.startswith('100644 ')and e.endswith(' 0\t'+n)
    assert g.git_bytes('show',':unsolved_math_prioritization/QUEUE.md')==g.Q.read_bytes()
    g.fresh_check(pre,{'unsolved_math_prioritization/QUEUE.md'})
    assert g.git('rev-parse','HEAD')==pre['main_before']and g.git('rev-parse','MERGE_HEAD')==g.HEAD
    print(json.dumps({'status':'PASS_EXACT506_STAGED_BODIES_MODES','overlay':505,'queue':1,'foreign_staged':0}))
if __name__=='__main__':main()
