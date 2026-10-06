#!/usr/bin/env python3
"""Read-only exact-snapshot binding checks; outputs JSON to stdout."""
from pathlib import Path
import hashlib,json,subprocess,sys,os,difflib

BASE=Path(__file__).resolve().parent.parent
R=BASE/'release'
EXPECTED={'MANIFEST.sha256':'15b87ed1e163d1f07d6d66dc8d32354b98aa3c62c6e218e8ee02790971099bb2','author/MANIFEST.sha256':'cba75811450e787073452b49549169d07316a5f4f5294de5524997236c017c63','author/PROOF.md':'697b031dfc8e7c65d83854d8dcf5bcbfc4f9000b6e8769166d6b38999f45f3f4','original_author/MANIFEST.sha256':'4a4a0478c91311606382e2ae00aa891d93272992593724e976589ab9ef65cf6c','independent_review/MANIFEST.sha256':'8673ca5bd15366eaa567d101f8ee18026957d202bd3b4eac53bf761e11ec40e9'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def manifest(d):
    m=d/'MANIFEST.sha256';entries={}
    for line in m.read_text().splitlines():
        h,name=line.split('  ',1)
        assert len(h)==64 and name not in entries
        assert not Path(name).is_absolute() and '..' not in Path(name).parts
        p=d/name;assert p.is_file() and not p.is_symlink() and sha(p)==h
        entries[name]=h
    files={str(p.relative_to(d)) for p in d.rglob('*') if p.is_file() and p!=m}
    assert files==set(entries),(files-set(entries),set(entries)-files)
    assert not any(p.is_symlink() for p in d.rglob('*'))
    return entries
for path,h in EXPECTED.items():assert sha(R/path)==h,(path,sha(R/path))
counts={str(d.relative_to(R)) if d!=R else '.':len(manifest(d)) for d in [R,R/'author',R/'original_author',R/'independent_review']}
def compare_dirs(a,b):
    aa={str(p.relative_to(a)):sha(p) for p in a.rglob('*') if p.is_file()}
    bb={str(p.relative_to(b)):sha(p) for p in b.rglob('*') if p.is_file()}
    assert aa==bb
    return len(aa)
preserved={'original_author':compare_dirs(BASE/'author',R/'original_author'),'independent_review':compare_dirs(BASE/'audit',R/'independent_review')}
changes={'ROUTES.md':('Equivalently, |A_j(f)|=1 forces f and xʲ−1 to be relatively prime after reduction modulo every rational prime.','Equivalently, |B_j(f)|=1 holds if and only if f and xʲ−1 are relatively prime after reduction modulo every rational prime; this is also equivalent to |A_m(f)|=1 for every m dividing j.'),'PROOF.md':('f=P(x+a)+r,   a∈Z, r∈R.','f(x)=P(x)(x+a)+r(x),   a∈Z, r∈R.')}
changed=[]
for p in sorted((R/'original_author').iterdir()):
    q=R/'author'/p.name
    if p.read_bytes()!=q.read_bytes():
        changed.append(p.name)
        if p.name!='MANIFEST.sha256':
            old,new=changes[p.name];s=p.read_text();assert s.count(old)==1
            assert s.replace(old,new)==q.read_text()
assert changed==['MANIFEST.sha256','PROOF.md','ROUTES.md']
assert (R/'corrections/APPLIED.patch').read_bytes()==(R/'independent_review/proposed_corrections.patch').read_bytes()
expected_diff=''
for name in ['PROOF.md','ROUTES.md']:
    expected_diff+=''.join(difflib.unified_diff((R/'original_author'/name).read_text().splitlines(True),(R/'author'/name).read_text().splitlines(True),fromfile='a/'+name,tofile='b/'+name))
assert expected_diff==(R/'corrections/DIFF.patch').read_text()
status=json.loads((R/'author/STATUS.json').read_text())
assert status['status']=='unsolved' and status['full_target_resolved'] is False and status['substantive_routes']==5
ledger=json.loads((R/'corrections/CORRECTION_LEDGER.json').read_text())
assert ledger['original_author_manifest_sha256']==EXPECTED['original_author/MANIFEST.sha256']
assert ledger['original_audit_manifest_sha256']==EXPECTED['independent_review/MANIFEST.sha256']
assert ledger['corrected_author_manifest_sha256']==EXPECTED['author/MANIFEST.sha256']
assert ledger['status']=='unsolved' and ledger['full_target_resolved'] is False and ledger['substantive_routes']==5
for change in ledger['changed_author_files']:
    assert sha(R/'original_author'/change['path'])==change['before_sha256']
    assert sha(R/'author'/change['path'])==change['after_sha256']
for filename,h in ledger['unchanged_mathematical_controls'].items():assert sha(R/'author'/filename)==h
# Reexecute without creating bytecode in the read-only reviewed trees.
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
runs=[]
for cwd,command,output in [(R/'author',[sys.executable,'verify.py'],R/'author/results.json'),(R/'author',[sys.executable,'crosscheck_sympy.py'],R/'author/CROSSCHECK.txt'),(R/'independent_review',[sys.executable,'independent_verify.py','--author-json','../author/results.json'],R/'independent_review/independent_results.json')]:
    proc=subprocess.run(command,cwd=cwd,env=env,capture_output=True,check=True)
    assert proc.stdout==output.read_bytes(),command
    runs.append({'command':command[1:],'expected_file':str(output.relative_to(R)),'output_sha256':hashlib.sha256(proc.stdout).hexdigest(),'byte_exact':True})
for path,h in EXPECTED.items():assert sha(R/path)==h
assert len(manifest(R))==counts['.']
print(json.dumps({'verdict':'ACCEPT_CORRECTED_SCOPED_RELEASE','bound_hashes':EXPECTED,'manifest_entry_counts':counts,'preserved_file_counts':preserved,'changed_author_files_including_manifest':changed,'exact_C1_C2_only':True,'applied_patch_matches_original_audit':True,'generated_diff_matches_exact_content_changes':True,'replays':runs,'release_unmodified':True,'full_target_status':'unsolved','full_target_resolved':False,'substantive_routes':5},indent=2,sort_keys=True))
