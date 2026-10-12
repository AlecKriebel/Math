from pathlib import Path
import hashlib,json,subprocess,datetime
R=Path(__file__).resolve().parent;W=Path('/Users/alec/Documents/Math');A=R.parent
H='391a2e306581b57e5a5ffbd177e8b9add894ad56';B='4342abee079cca889f9e98873ac36c29a3de3645';O='421c6aa90eace49c8659f9a96e83c24fe1b5b901';M='429e3f91097238669be7fc2173b9ce4d9956a3af'
def git(*args):return subprocess.check_output(['git',*args],cwd=W)
def sha(b):return hashlib.sha256(b).hexdigest()
m=json.loads((A/'repaired_snapshot_manifest.json').read_text());assert (m['head'],m['base'],m['original_frozen_head'])==(H,B,O)
files=[]
for e in m['files']:
 b=(A/'repaired_snapshot'/e['path']).read_bytes();g=git('show',f"{H}:{e['path']}")
 assert b==g and len(b)==e['bytes'] and sha(b)==e['sha256']
 target=e['path'].startswith('unsolved_math_prioritization/attempts/6600013/')
 same=None
 if target:same=b==git('show',f"{O}:{e['path']}");assert same
 files.append({'path':e['path'],'bytes':len(b),'sha256':sha(b),'git_blob_sha1':sha(b) if False else hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(),'same_original':same})
assert len(files)==58 and sum(x['same_original'] is True for x in files)==57
parents=git('show','-s','--format=%P',H).decode().strip().split();assert parents==[O,B]
baseparents=git('show','-s','--format=%P',B).decode().strip().split()
assert subprocess.run(['git','merge-base','--is-ancestor',M,B],cwd=W).returncode==0
q='unsolved_math_prioritization/QUEUE.md';old=git('show',f'{B}:{q}');new=git('show',f'{H}:{q}');a=old.splitlines(keepends=True);b=new.splitlines(keepends=True)
assert len(a)==len(b)
changed=[i+1 for i,(x,y) in enumerate(zip(a,b)) if x!=y];assert changed==[418]
oldcells=a[417].split(b'|');newcells=b[417].split(b'|');changedcells=[i for i,(x,y) in enumerate(zip(oldcells,newcells)) if x!=y]
assert changedcells==[8,9]
assert oldcells[2]==newcells[2] and b'6600013' in newcells[2]
assert newcells[8].strip()==b'unsolved' and newcells[9].strip()==b'5/5'
rows={'line':418,'changed_physical_pipe_cells':changedcells,'base_row':a[417].decode(),'head_row':b[417].decode(),'all_other_lines_equal':True,'all_other_target_cells_equal':True,'base_sha256':sha(old),'head_sha256':sha(new)}
paths=git('diff','--name-only',B,H).decode().splitlines();assert set(paths)=={e['path'] for e in m['files']}
rawcount=sum(Path(e['path']).suffix.lower()=='.pdf' for e in m['files']);assert rawcount==0
receipt={'timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat(),'head':H,'actual_main':B,'original_head':O,'head_parents':parents,'base_parents':baseparents,'actual_PR383_merge':M,'PR383_is_ancestor_of_actual_main':True,'manifest_files':58,'unchanged_original_target_files':57,'exact_base_diff_paths':paths,'queue':rows,'public_raw_source_count':rawcount,'files':files}
(R/'BINDING_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps({k:v for k,v in receipt.items() if k not in ['files','exact_base_diff_paths']},indent=2))
