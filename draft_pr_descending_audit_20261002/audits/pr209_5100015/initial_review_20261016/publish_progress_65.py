"""Publish accepted second scientific review; no release/PR/queue mutations."""
from pathlib import Path
import ast, hashlib, json

D=Path(__file__).resolve().parent
p=D/'publish_progress_55.py'
t=ast.parse(p.read_text())
assert isinstance(t.body[-1],ast.Expr)
t.body=[n for n in t.body[:-1] if not (isinstance(n,ast.Assert) and 'PROGRESS_55_CHECKPOINT_RECEIPT' in ast.unparse(n))]
ns={'__file__':str(p)}
exec(compile(t,str(p)+'[definitions-only]','exec'),ns)
source=ns['source']
assert not (D/'PROGRESS_65_CHECKPOINT_RECEIPT.json').exists()
extra="""folder=D.parent/'whole_package_adversary_02'
seal=folder/'AUTHORED_MANIFEST.json';m=json.loads(seal.read_text());paths.append(seal)
assert hashlib.sha256(seal.read_bytes()).hexdigest()=='217d7efee050e8bfffeb5ba88a43177ceb36d5f7173cd4f46b708248ad1faf09'
for row in m['files']:
    q=folder/row['path'];raw=q.read_bytes()
    assert q.resolve().is_relative_to(folder.resolve()) and not q.is_symlink()
    assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256']
    paths.append(q)
for name in ['root_reproduction_08_release_helpers_review01','root_reproduction_09_whole_review02']:
    paths += [q for q in (D/name).iterdir() if q.is_file()]
"""
changes=[
 ("OUT=D/'PROGRESS_55_CHECKPOINT_RECEIPT.json'","OUT=D/'PROGRESS_65_CHECKPOINT_RECEIPT.json'"),
 ("prior=json.loads((D/'PROGRESS_45_CHECKPOINT_RECEIPT.json').read_text())","prior=json.loads((D/'PROGRESS_55_CHECKPOINT_RECEIPT.json').read_text())"),
 ("assert prior['commit']=='d03508747f8fefc94f18793909372c16c3cd4ba8'","assert prior['commit']=='4d58dd0557c1108ac6ea24395deb28cf560d9303'"),
 ("assert state['completion_percent']==55 and state['preprint_preparation_cleared'] is True","assert state['completion_percent']==65 and state['preprint_preparation_cleared'] is True"),
 ("strftime('progress55_%Y%m%dT%H%M%S%fZ')","strftime('progress65_%Y%m%dT%H%M%S%fZ')"),
 ("paths += [OLD/'FINAL_COMPLETION_CHECKPOINT_PUBLICATION_RECEIPT.json'",extra+"paths += [OLD/'FINAL_COMPLETION_CHECKPOINT_PUBLICATION_RECEIPT.json'"),
 ("assert len(entries)<750","assert len(entries)<1500"),
 ("Checkpoint PR209 at55%: first whole-package repair and real ZIP replay; new review active, workflow findings open","Checkpoint PR209 at65%: two scientific package reviews accepted; final clean controls reproduced; source repairs pending"),
 ("case_completion_percent=55","case_completion_percent=65"),
]
for old,new in changes:
    assert source.count(old)==1,old
    source=source.replace(old,new)
# This checkpoint adds more than 300 paths. Inspect the complete native tree
# delta; GitHub's comparison-file cap is never evidence of complete scope.
old="""delta=api('GET','compare/'+parent+'...'+new)
assert delta['status']=='ahead' and delta['total_commits']==1 and len(delta['files'])<300
assert {x['filename'] for x in delta['files']}<=set(expected)
assert all(x['status']!='removed' for x in delta['files'])"""
new="""native_cache={}
def native_rows(tree):
    if tree not in native_cache:
        obj=api('GET','git/trees/'+tree)
        assert obj.get('truncated') is False
        rows=obj['tree'];assert len(rows)==len({x['path'] for x in rows})
        native_cache[tree]={x['path']:{k:x[k] for k in ('type','mode','sha')} for x in rows}
    return native_cache[tree]
def full_delta(left,right,prefix=''):
    if left==right:return []
    a=native_rows(left) if left else {};b=native_rows(right) if right else {};out=[]
    for name in sorted(set(a)|set(b)):
        x,y=a.get(name),b.get(name)
        if x==y:continue
        if (x is None or x['type']=='tree') and (y is None or y['type']=='tree'):
            out+=full_delta(x['sha'] if x else None,y['sha'] if y else None,prefix+name+'/')
        else:
            assert (x is None or x['type']=='blob') and (y is None or y['type']=='blob'),'Unexpected tree/type replacement'
            out.append(dict(filename=prefix+name,status='removed' if y is None else 'added' if x is None else 'modified',old=x,new=y))
    return out
delta={'files':full_delta(commit['tree']['sha'],tree)}
assert {x['filename'] for x in delta['files']}<=set(expected)
for row in delta['files']:
    assert row['status']!='removed'
    raw=expected[row['filename']]
    assert row['new']==dict(type='blob',mode='100644',sha=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\\0'+raw).hexdigest())
"""
assert source.count(old)==1
source=source.replace(old,new)
exec(compile(source,str(D/'publish_progress_65.py')+'[pinned-template]','exec'),{'__file__':str(D/'publish_progress_65.py'),'__name__':'__main__'})
