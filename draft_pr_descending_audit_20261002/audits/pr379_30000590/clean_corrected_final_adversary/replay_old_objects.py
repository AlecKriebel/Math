#!/usr/bin/env python3
"""Replay the superseded wrapper using only bytes from its actual Git object."""
import hashlib,json,subprocess,sys,datetime
from pathlib import Path
HERE=Path(__file__).absolute().parent
COMMIT='90794508688ec07f598e0871bbd1eb38aaf466ce'
TARGET='problems/30000590_group_ring_cohomology'
REPO='/Users/alec/Documents/Math'
ROOT=HERE/'private_replay/original_git_head'
OUT=HERE/'replay_outputs'
files=subprocess.check_output(['git','-C',REPO,'ls-tree','-r','--name-only',COMMIT,'--',TARGET]).decode().splitlines()
assert len(files)==55
bindings=[]
for name in files:
    data=subprocess.check_output(['git','-C',REPO,'show',COMMIT+':'+name])
    dest=ROOT/Path(name).relative_to(TARGET)
    dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
    bindings.append({'path':name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
receipts=[]
for label,args in [('original_publication_no_sources',[]),('original_publication_with_fresh_sources',['--source-dir',str(HERE/'raw_sources/source_aliases')])]:
    cmd=[sys.executable,str(ROOT/'verify_publication.py'),*args]
    start=datetime.datetime.now(datetime.timezone.utc).isoformat()
    r=subprocess.run(cmd,cwd=ROOT,capture_output=True)
    a,b=OUT/(label+'.stdout.txt'),OUT/(label+'.stderr.txt')
    a.write_bytes(r.stdout);b.write_bytes(r.stderr)
    receipts.append({'label':label,'commit':COMMIT,'command':cmd,'start_utc':start,'end_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit_code':r.returncode,'script_sha256':hashlib.sha256((ROOT/'verify_publication.py').read_bytes()).hexdigest(),'stdout':str(a.relative_to(HERE)),'stderr':str(b.relative_to(HERE)),'stdout_bytes':len(r.stdout),'stderr_bytes':len(r.stderr),'stdout_sha256':hashlib.sha256(r.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(r.stderr).hexdigest()})
    assert r.returncode==0 and not r.stderr,label
for e in bindings:
    assert hashlib.sha256((ROOT/Path(e['path']).relative_to(TARGET)).read_bytes()).hexdigest()==e['sha256']
result={'status':'PASS','original_head':COMMIT,'actual_object_files':55,'private_object_copy_unchanged':True,'complete_runs':receipts,'object_bindings':bindings,'claim_scope':'Historical reproduction only. Historical unqualified graph wording remains superseded.'}
print(json.dumps(result,indent=2))
