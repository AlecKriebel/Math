"""Stage only the reviewed canonical bodies and whole accepted QUEUE."""
from pathlib import Path
import hashlib,json,subprocess,sys
A=Path(__file__).resolve().parent; R=A.parents[2]
sys.dont_write_bytecode=True; sys.path.insert(0,str(A/'acceptance_preparation_family'))
import pr47_guards as g
def main():
    assert __debug__
    pre=g.load(A/'integration_preflight.json'); overlay=g.load(A/'integration_check.json')
    assert g.git('rev-parse','HEAD')==pre['main_before'] and g.git('rev-parse','MERGE_HEAD')==g.HEAD
    rr=overlay['canonical_overlay_files']; assert len(rr)==1337
    g.check(g.K,rr); g.fresh_check(pre,{'unsolved_math_prioritization/QUEUE.md'})
    prefix=g.K.relative_to(R).as_posix()+'/'
    names={prefix+z['path'] for z in rr}|{'unsolved_math_prioritization/QUEUE.md'}
    staged=set(g.git_bytes('diff','--cached','--name-only','-z').decode().split('\0'))-{''}
    assert staged<=names,staged-names
    subprocess.run(['git','add','-f','--',*sorted(names)],cwd=R,check=True)
    assert not g.git('diff','--name-only','--diff-filter=U')
    actual=set(g.git_bytes('diff','--cached','--name-only','-z').decode().split('\0'))-{''}; assert actual==names
    entries={}
    for e in g.git_bytes('ls-files','--stage','-z','--',*sorted(names)).split(b'\0'):
        if not e:continue
        fields,n=e.split(b'\t',1);mode,oid,stage=fields.split();assert mode==b'100644' and stage==b'0';entries[n.decode()]=oid.decode()
    assert set(entries)==names
    for n in names:
        raw=(R/n).read_bytes(); oid=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(); assert entries[n]==oid
    assert g.sha(g.Q.read_bytes())==overlay['whole_queue_after_sha256']
    g.fresh_check(pre,{'unsolved_math_prioritization/QUEUE.md'})
    assert g.git('rev-parse','HEAD')==pre['main_before'] and g.git('rev-parse','MERGE_HEAD')==g.HEAD
    print(json.dumps(dict(status='PASS_EXACT_SELECTED_STAGED_BODIES_MODES',overlay=len(rr),queue=1,foreign_staged=0)))
if __name__=='__main__':main()
