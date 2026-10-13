"""Refresh the reviewed claimed-solved PR without touching the shared checkout.

Requires two completed fresh preprint reviews. Preserve all 37 submitted mathematical
files exactly, add the cleared submission, and reconcile only our status/turn/note cells.
"""
from pathlib import Path
import datetime,hashlib,json,os,subprocess,time
A=Path(__file__).resolve().parent;P=A.parents[1];R=P.parent
Q='unsolved_math_prioritization/QUEUE.md';N=359;PROBLEM=b'30001370'
H='6be98eac0ba508368218179ecf80020c037dbece'
BRANCH='math/30001370-basin-boundaries-reviewed'
utc=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
sha=lambda b:hashlib.sha256(b).hexdigest()
load=lambda p:json.loads(p.read_bytes())
assert not load(P/'SHARED_GIT_WINDOW_STATUS.json')['shared_git_writes_paused'],"Respect the ascending reviewer's shared Git window."
original=load(A/'snapshot_manifest.json');assert original['head']==H
expected={e['path'] for e in original['files']};assert len(expected)==38
clear=load(A/'PUBLISHING_CLEARANCE.json')
assert clear['status']=='READY_AFTER_TWO_SEQUENTIAL_FRESH_PREPRINT_REVIEWS'
assert clear['second_review_mandatory_findings']==0
for e in clear['sealed_submission_files']:
 b=(A/'preprint'/e['path']).read_bytes();assert len(b)==e['bytes'] and sha(b)==e['sha256']
D=A/'root_replay_private'/('queue_refresh_'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%f'));D.mkdir(parents=True,exist_ok=False)
captures=[]
def run(tag,args,ok=(0,),input=None):
 if args[0]=='git' and args[1] in {'fetch','hash-object','mktree','commit-tree','push'}:assert not load(P/'SHARED_GIT_WINDOW_STATUS.json')['shared_git_writes_paused']
 start=utc();r=subprocess.run(args,cwd=R,input=input,capture_output=True,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0',GIT_NO_LAZY_FETCH='1'))
 streams={}
 for name,b in [('stdout',r.stdout),('stderr',r.stderr)]:
  path=D/(tag+'.'+name);path.write_bytes(b);streams[name]={'path':str(path.relative_to(A)),'bytes':len(b),'sha256':sha(b)}
 c={'tag':tag,'argv':args,'started_utc':start,'finished_utc':utc(),'exit_code':r.returncode,'streams':streams};captures.append(c);(D/(tag+'.json')).write_text(json.dumps(c,indent=2)+'\n')
 assert r.returncode in ok,(tag,r.returncode,r.stderr.decode(errors='replace'));return r
counter=0
def git(*args,input=None,ok=(0,)):
 global counter
 counter+=1;return run('git_'+str(counter),['git',*args],ok,input).stdout
assert git('branch','--show-current').strip()==b'main'
assert subprocess.run(['git','rev-parse','-q','--verify','MERGE_HEAD'],cwd=R,capture_output=True).returncode!=0
ix=Path(git('rev-parse','--git-path','index').decode().strip());ix=ix if ix.is_absolute() else R/ix;index=ix.read_bytes()
local=git('rev-parse','HEAD').decode().strip()
pr=json.loads(run('remote_before',['gh','pr','view',str(N),'--json','state,headRefOid,isDraft,headRefName']).stdout)
assert pr['state']=='OPEN' and pr['headRefName']==BRANCH
old=pr['headRefOid']
if old!=H:
 prior=load(A/'repaired_snapshot_manifest.json');assert prior['head']==old and prior['original_frozen_head']==H
 archive=A/'queue_refresh_history'/old;archive.mkdir(parents=True,exist_ok=False)
 for name in ['repaired_snapshot_manifest.json','queue_repair_receipt.json','root_exact_live_receipt.json']:
  f=A/name
  if f.exists():(archive/name).write_bytes(f.read_bytes())
 (A/'repaired_snapshot').rename(archive/'repaired_snapshot')
else:assert pr['isDraft']
for e in original['files']:
 if e['path']==Q:continue
 b=git('show',f"{old}:{e['path']}");assert len(b)==e['bytes'] and sha(b)==e['sha256']
 mode=git('ls-tree',old,'--',e['path']).split(b'\t',1)[0].split();assert mode[:2]==[b'100644',b'blob'] and mode[2].decode()==e['git_blob_sha']
run('main_fetch',['git','fetch','origin','main'])
main=git('rev-parse','origin/main').decode().strip();assert main==local,'Shared main differs; do not alter it.'
v=run('merge_tree',['git','merge-tree','--write-tree',old,main],ok=(0,1));tree=v.stdout.decode().splitlines()[0]
if v.returncode:
 conflicts=[line.rsplit('\t',1)[1] for line in v.stdout.decode().splitlines() if '\t' in line]
 assert conflicts and set(conflicts)=={Q},conflicts
def row(lines):
 found=[i for i,b in enumerate(lines) if len(b.split(b'|'))>11 and b.split(b'|')[2].strip().split(b' / ')[0]==PROBLEM]
 assert len(found)==1;return found[0]
frozen=git('show',f'{H}:{Q}').splitlines(keepends=True);fc=frozen[row(frozen)].split(b'|')
assert [fc[i].strip() for i in (8,9)]==[b'claimed_solved',b'3/5']
raw=git('show',f'{main}:{Q}');lines=raw.splitlines(keepends=True);i=row(lines);before=lines[i];cells=before.split(b'|')
assert [cells[j].strip() for j in (8,9)]==[b'queued',b'0/5']
for j in (8,9):cells[j]=fc[j]
cells[11]=b' '+cells[11].strip()+b' Verified common L1 basin boundaries; six-page research note and verification supplement ready; bounded priority and two fresh AI preprint reviews passed (unrefereed). '
assert [j for j,(x,y) in enumerate(zip(before.split(b'|'),cells)) if x!=y]==[8,9,11]
lines[i]=b'|'.join(cells);new=b''.join(lines)
def replace(tree,parts,blob):
 entries={}
 for item in git('ls-tree','-z',tree).split(b'\0'):
  if item:
   meta,name=item.split(b'\t',1);mode,kind,oid=meta.split();entries[name]=(mode,kind,oid)
 name=parts[0].encode();prior=entries.get(name)
 if len(parts)==1:
  if prior:assert prior[:2]==(b'100644',b'blob')
  entries[name]=(b'100644',b'blob',blob.encode())
 else:
  if prior:assert prior[:2]==(b'040000',b'tree');child=prior[2].decode()
  else:child=git('mktree','-z',input=b'').decode().strip()
  entries[name]=(b'040000',b'tree',replace(child,parts[1:],blob).encode())
 return git('mktree','-z',input=b''.join(b' '.join(entries[n])+b'\t'+n+b'\0' for n in sorted(entries))).decode().strip()
blob=git('hash-object','-w','--stdin',input=new).decode().strip();tree=replace(tree,Q.split('/'),blob)
submission_scope={}
for e in clear['sealed_submission_files']:
 path='problems/30001370_basin_boundaries/preprint/'+e['path']
 b=(A/'preprint'/e['path']).read_bytes();submission_scope[path]=b
 assert len(b)==e['bytes'] and sha(b)==e['sha256']
release=('Verified research note for OWR-4132-003 (30001370)\n\n'
 'The exact stated tanh/Mobius common L1 basin-boundary conjecture is proved on all probability densities. '
 'The global convergence theorem, analytic-core boundary seed and inverse-expansion method are credited prior results. '
 'The new closure construction and open-map proof handle unbounded densities and zeros.\n\n'
 'Three independent mathematical approach families, a bounded primary-literature comparison, and two sequential fresh full preprint adversaries were completed. '
 'No equivalent earlier result was found in the inspected corpus; this is not a global priority certificate. '
 'The final foundational journal proof version was not obtained. '
 'AI tools were used extensively; this note is unrefereed and has not received independent external human peer review.\n\n'
 'The 37 submitted problem artifacts below remain byte-identical to original head '+H+'. '
 'Their historical turn/state/review metadata are preserved, and are not new execution receipts. '
 'The four files in preprint/ are the cleared current submission. Production Zenodo publication and Google tracker registration are recorded separately when completed.\n\n'
 'Cleared submission files:\n'+''.join('- '+e['path']+': '+str(e['bytes'])+' bytes; SHA256 '+e['sha256']+'\n' for e in clear['sealed_submission_files'])+'\n'
 'Fresh review bindings: see audit-program PUBLISHING_CLEARANCE.json and root verification receipts.\n'
 'License: CC BY 4.0. Author: Alec Kriebel, ORCID0009-0001-9320-500X.\n').encode()
submission_scope['problems/30001370_basin_boundaries/PREPRINT_RELEASE.md']=release
assert len(submission_scope)==5
for path,b in submission_scope.items():
 oid=git('hash-object','-w','--stdin',input=b).decode().strip();tree=replace(tree,path.split('/'),oid)
expected|=set(submission_scope);assert len(expected)==43
assert set(git('diff','--name-only',main,tree).decode().splitlines())==expected
for e in original['files']:
 if e['path']!=Q:
  b=git('show',f"{tree}:{e['path']}");assert len(b)==e['bytes'] and sha(b)==e['sha256']
  meta=git('ls-tree',tree,'--',e['path']).split(b'\t',1)[0].split();assert meta==[b'100644',b'blob',e['git_blob_sha'].encode()]
for path,b in submission_scope.items():assert git('show',f'{tree}:{path}')==b
assert git('show',f'{tree}:{Q}')==new
assert git('rev-parse','HEAD').decode().strip()==local and ix.read_bytes()==index
last=json.loads(run('remote_main_before_push',['gh','api','repos/AlecKriebel/Math/git/ref/heads/main']).stdout)
assert last['object']['sha']==main
commit=git('commit-tree',tree,'-p',old,'-p',main,input=b'Refresh PR359 against current main; preserve submitted proof, add cleared preprint and reconcile own queue cells\n').decode().strip()
run('branch_push',['git','push','origin',f'{commit}:refs/heads/{BRANCH}'])
assert git('rev-parse','HEAD').decode().strip()==local and ix.read_bytes()==index
after=json.loads(run('remote_after',['gh','pr','view',str(N),'--json','state,headRefOid,headRefName']).stdout)
if after['headRefOid']!=commit:
 ref=json.loads(run('branch_ref_after_push',['gh','api',f'repos/AlecKriebel/Math/git/ref/heads/{BRANCH}']).stdout)
 assert ref['object']['sha']==commit,'Do not repeat an uncertain branch mutation.'
 for attempt in range(6):
  time.sleep(0.5)
  after=json.loads(run('remote_after_readonly_retry_'+str(attempt),['gh','pr','view',str(N),'--json','state,headRefOid,headRefName']).stdout)
  if after['headRefOid']==commit:break
assert after['state']=='OPEN' and after['headRefOid']==commit and after['headRefName']==BRANCH
S=A/'repaired_snapshot';files=[]
for path in sorted(expected):
 b=git('show',f'{commit}:{path}');f=S/path;f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(b)
 meta=git('ls-tree',commit,'--',path).split(b'\t',1)[0].split();assert meta[:2]==[b'100644',b'blob']
 files.append({'path':path,'bytes':len(b),'sha256':sha(b),'git_blob_sha':meta[2].decode(),'mode':'100644'})
m={'pr':N,'head':commit,'base':main,'original_frozen_head':H,'previous_review_head':old,'frozen_utc':utc(),'files':files}
(A/'repaired_snapshot_manifest.json').write_text(json.dumps(m,indent=2)+'\n')
receipt={'utc':utc(),'status':'PASS_CLAIMED_SOLVED_QUEUE_REFRESH','pr':N,'original_head':H,'previous_review_head':old,'repaired_head':commit,'current_main_parent':main,'parents':[old,main],'tree':tree,'all_original_target_files_unchanged':37,'new_submission_files':5,'changed_queue_line':i+1,'changed_queue_pipe_cells':[8,9,11],'accepted_status':'claimed_solved','author_turns':'3/5','old_row':before.decode(),'new_row':lines[i].decode(),'all_other_queue_bytes_preserved':True,'checkout_and_entire_index_unchanged':True,'nonforce_branch_push_succeeded':True,'captures':captures,'program_sha256':sha(Path(__file__).read_bytes())}
(A/'queue_repair_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
for f in [A/'RESEARCH_LOG.md',P/'RESEARCH_LOG.md']:
 with f.open('a') as h:h.write(f'\n{receipt["utc"]}: PR359 original37 mathematical files unchanged; cleared4 submission files and release note added; queue refresh `{commit}` against `{main}` changed only own line{i+1} cells8,9,11. Main checkout and entire shared index preserved. Mathematical resolution100%, preprint preparation100%; acceptance/publication workflow80%, exact-live/actual-merge/Zenodo/tracker remain pending.\n')
print(json.dumps({k:v for k,v in receipt.items() if k!='captures'},indent=2))
