"""Recover the completed PR367 branch push after a local ENOSPC failure.
No Git or remote mutation; prove the full scope before rebuilding local copies.
"""
import datetime, hashlib, json, subprocess
from pathlib import Path
P=Path(__file__).resolve().parent
A=P/'audits/pr367_11000151'
HEAD='cb1e5cff9a02649e59cbb60f7369d6281de3d703'
BASE='f63a97ada19c9b377e7aa2073d30e301f94a4c45'
QUEUE='unsolved_math_prioritization/QUEUE.md'
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*args):return subprocess.check_output(['git',*args])
def write(p,o):p.write_text(json.dumps(o,indent=2)+'\n')
def api(label,path):
 r=subprocess.run(['gh','api','--method','GET','-H','Cache-Control: no-cache','repos/AlecKriebel/Math/'+path],capture_output=True)
 (A/('recovery_'+label+'.stdout')).write_bytes(r.stdout)
 (A/('recovery_'+label+'.stderr')).write_bytes(r.stderr)
 assert r.returncode==0 and r.stderr==b''
 return json.loads(r.stdout)
original=json.loads((A/'snapshot_manifest.json').read_bytes())
old=original['head']
assert git('branch','--show-current')==b'main\n'
assert git('rev-parse','HEAD').decode().strip()==BASE
assert git('rev-list','--parents','-n','1',HEAD).decode().split()==[HEAD,old,BASE]
pr=api('pr','pulls/367');main=api('main','git/ref/heads/main')
assert pr['state']=='open' and pr['draft'] is True and pr['head']['sha']==HEAD
assert pr['base']['sha']==main['object']['sha']==BASE
assert pr['base']['ref']=='main' and pr['head']['ref']=='math/11000151-artin-a5-quotient-wip'
expected={r['path'] for r in original['files']}
assert set(git('diff','--name-only',BASE,HEAD).decode().splitlines())==expected
files=[]
for row in original['files']:
 path=row['path'];data=git('show',HEAD+':'+path)
 mode,kind,blob,_=git('ls-tree',HEAD,'--',path).decode().split(None,3)
 assert mode=='100644' and kind=='blob'
 if path!=QUEUE:
  assert data==git('show',old+':'+path)==(A/'snapshot'/path).read_bytes()
  assert len(data)==row['bytes'] and sha(data)==row['sha256'] and blob==row['git_blob_sha']
 files.append({'path':path,'bytes':len(data),'sha256':sha(data),'git_blob_sha':blob,'mode':mode})
before=git('show',BASE+':'+QUEUE);after=git('show',HEAD+':'+QUEUE)
lines=before.splitlines(keepends=True);newlines=after.splitlines(keepends=True)
assert len(lines)==len(newlines)
assert [i+1 for i,(x,y) in enumerate(zip(lines,newlines)) if x!=y]==[400]
cells=lines[399].split(b'|');assert b'11000151 / AMR-109-0151' in cells[2]
assert cells[8:10]==[b' queued ',b' 0/5 ']
cells[8:10]=[b' claimed_solved ',b' 4/5 '];expected_lines=list(lines);expected_lines[399]=b'|'.join(cells)
assert after==b''.join(expected_lines)
tree=git('rev-parse',HEAD+'^{tree}').decode().strip()
assert git('merge-tree','--write-tree',BASE,HEAD).decode().splitlines()[0]==tree
for row in files:
 path=row['path'];data=git('show',HEAD+':'+path);p=A/'repaired_snapshot'/path
 p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
 assert p.read_bytes()==data and len(data)==row['bytes'] and sha(data)==row['sha256']
assert {p.relative_to(A/'repaired_snapshot').as_posix() for p in (A/'repaired_snapshot').rglob('*') if p.is_file()}==expected
end=api('end_pr','pulls/367');endmain=api('end_main','git/ref/heads/main')
assert end['state']=='open' and end['draft'] is True and end['head']['sha']==HEAD
assert end['base']['sha']==endmain['object']['sha']==BASE
t=utc()
write(A/'repaired_snapshot_manifest.json',{'pr':367,'head':HEAD,'base':BASE,'original_frozen_head':old,'previous_review_head':old,'frozen_utc':t,'target_prefix':original['target_prefix'],'files':files,'recovered_after_local_ENOSPC':True})
receipt={'utc':t,'pr':367,'original_head':old,'previous_review_head':old,'repaired_head':HEAD,'current_main_parent':BASE,'parents':[old,BASE],'tree':tree,'all_original_target_files_unchanged':43,'changed_queue_line':400,'changed_queue_pipe_cells':[8,9],'accepted_status':'claimed_solved','author_turns':'4/5','old_row':lines[399].decode(),'new_row':newlines[399].decode(),'all_other_queue_bytes_preserved':True,'nonforce_branch_push_succeeded':True,'local_snapshot_recovered_and_all44_bytes_verified':True,'raw_source_count':0,'exact_live_review_pending':True}
write(A/'queue_repair_receipt.json',receipt)
v1=json.loads((A/'ROOT_CLAIMED_REFRESH_FAILURES.json').read_bytes())
write(A/'ROOT_CLAIMED_REFRESH_FAILURES_v1.json',v1)
v2bytes=(P/'root_refresh_claimed_solved_queue.py').read_bytes()
(P/'root_refresh_claimed_solved_queue_v2.py').write_bytes(v2bytes)
write(A/'ROOT_CLAIMED_REFRESH_FAILURES.json',{'utc':t,'attempts':[v1,{'status':'NONFORCE_BRANCH_PUSH_SUCCEEDED_LOCAL_SNAPSHOT_WRITE_FAILED_NO_ACCEPTANCE_CREDIT','cause':'Shared disk ENOSPC writing STATE_T4.json after branch push','preserved_program':'root_refresh_claimed_solved_queue_v2.py','program_sha256':sha(v2bytes),'actual_pushed_head':HEAD,'base':BASE,'original43_mathematical_files_unchanged':True,'recovery':'root_recover_claimed_refresh.py independently verified parents, exact44 scope, every43 original byte/mode/blob and full queue, then rebuilt all44 complete local files','recovery_receipt':'queue_repair_receipt.json'}]})
inv=json.loads((P/'inventory.json').read_bytes());row=next(r for r in inv['items'] if r['number']==367)
row.update(original_frozen_head=old,current_review_head=HEAD,disposition='queue_repaired_fresh_whole_package_review_pending',audit_workflow_percent=90)
write(P/'inventory.json',inv)
for p in [P/'RESEARCH_LOG.md',A/'RESEARCH_LOG.md',A/'README.md']:
 with p.open('a') as f:f.write('\n'+t+': Recovered completed PR367 nonforce refresh after postpush ENOSPC. All43 original mathematical blobs/modes and the entire44-path delta independently verified; own queue physical line400 cells8/9 only. Complete local frozen snapshot rebuilt. Workflow90%, fixed-input resolution100%; exact live acceptance, actual merge, Zenodo and tracker still pending. No acceptance credit for failed writes.\n')
print(json.dumps(receipt,indent=2))
