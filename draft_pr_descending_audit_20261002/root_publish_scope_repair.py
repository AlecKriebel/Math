"""Publish a prepared additive scope correction through a private Git index."""
import datetime,hashlib,json,os,subprocess,sys,uuid
from pathlib import Path
P=Path(__file__).resolve().parent; A=P/'audits'/sys.argv[1]
n=int(sys.argv[2]); problem=sys.argv[3]; input_manifest=sys.argv[4]
resume=sys.argv[5] if len(sys.argv)>5 else None
m=json.loads((A/input_manifest).read_text());old=m['head']
prep=json.loads((A/'scope_repair_preparation_receipt.json').read_text())
D=Path(prep['private_packet']);queue='unsolved_math_prioritization/QUEUE.md'
changed=prep['original_files_preserved_except_current_wrappers'];added=prep['new_files']
target=next(e['path'].rsplit('/',1)[0] for e in m['files'] if e['path'].startswith('problems/') and '/' not in e['path'][len('problems/'):].rsplit('/',1)[0])
expected={e['path'] for e in m['files']}|{target+'/'+x for x in added}
def git(*args,input=None,env=None):return subprocess.check_output(['git',*args],input=input,env=env)
def run(args,tag,ok=(0,)):
 r=subprocess.run(args,capture_output=True);(A/(tag+'.stdout')).write_bytes(r.stdout);(A/(tag+'.stderr')).write_bytes(r.stderr)
 assert r.returncode in ok,(tag,r.returncode,r.stderr.decode());return r
assert git('branch','--show-current').strip()==b'main'
r=json.loads(run(['gh','pr','view',str(n),'--json','state,headRefOid,isDraft,headRefName'],'scope_remote_resume' if resume else 'scope_remote').stdout)
assert r['state']=='OPEN' and r['headRefOid']==(resume or old) and r['isDraft']
run(['git','fetch','origin','main'],'scope_main_fetch_resume' if resume else 'scope_main_fetch')
if resume:
 parents=git('show','-s','--format=%P',resume).decode().strip().split();assert len(parents)==2 and parents[0]==old
 main=parents[1];assert subprocess.run(['git','merge-base','--is-ancestor',main,'origin/main']).returncode==0
else:main=git('rev-parse','origin/main').decode().strip()
v=run(['git','merge-tree','--write-tree',old,main],'scope_merge_tree',ok=(0,1));tree=v.stdout.decode().splitlines()[0]
if v.returncode:
 conflicts=[x.rsplit('\t',1)[1] for x in v.stdout.decode().splitlines() if '\t' in x]
 assert conflicts and set(conflicts)=={queue},conflicts
raw=git('show',f'{main}:{queue}');lines=raw.splitlines(keepends=True)
match=[i for i,l in enumerate(lines) if len(l.split(b'|'))>9 and l.split(b'|')[2].strip().split(b' / ')[0].decode()==problem]
assert len(match)==1;idx=match[0];before=lines[idx];cells=before.split(b'|')
assert [cells[i].strip() for i in (8,9)]==[b'queued',b'0/5']
cells[8]=b' unsolved ';cells[9]=b' 5/5 ';lines[idx]=b'|'.join(cells);new=b''.join(lines)
tmp=A/'tmp';tmp.mkdir(exist_ok=True);index=(tmp/('scope-index-'+uuid.uuid4().hex)).absolute();env=dict(os.environ,GIT_INDEX_FILE=str(index))
git('read-tree',tree,env=env)
def insert(path,b):
 blob=git('hash-object','-w','--stdin',input=b).decode().strip();git('update-index','--add','--cacheinfo',f'100644,{blob},{path}',env=env)
insert(queue,new)
for name in changed+added:insert(target+'/'+name,(D/name).read_bytes())
tree=git('write-tree',env=env).decode().strip()
paths=set(git('diff','--name-only',main,tree).decode().splitlines());assert paths==expected,(paths-expected,expected-paths)
preserved=[]
for e in m['files']:
 if e['path']!=queue and e['path'] not in {target+'/'+x for x in changed}:
  assert git('show',f"{tree}:{e['path']}")==git('show',f"{old}:{e['path']}"),e['path'];preserved.append(e['path'])
for name in changed+added:assert git('show',f'{tree}:{target}/{name}')==(D/name).read_bytes(),name
if resume:
 commit=resume;assert git('show','-s','--format=%T',commit).decode().strip()==tree
else:
 commit=git('commit-tree',tree,'-p',old,'-p',main,input=f'Qualify PR{n} current scope; preserve historical mathematics and all other queue entries\n'.encode()).decode().strip()
 (A/'scope_push_intent.json').write_text(json.dumps({'commit':commit,'parents':[old,main],'tree':tree,'branch':r['headRefName']},indent=2)+'\n')
 run(['git','push','origin',f"{commit}:refs/heads/{r['headRefName']}"],'scope_push')
remote=json.loads(run(['gh','pr','view',str(n),'--json','state,headRefOid,isDraft'],'scope_remote_after_recovery' if resume else 'scope_remote_after').stdout)
assert remote['state']=='OPEN' and remote['headRefOid']==commit and remote['isDraft']
S=A/'scope_repaired_snapshot';files=[]
for path in sorted(paths):
 b=git('show',f'{commit}:{path}');f=S/path;f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(b)
 files.append({'path':path,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'git_blob_sha':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()})
t=datetime.datetime.now(datetime.timezone.utc).isoformat()
out={'pr':n,'head':commit,'base':main,'previous_review_head':old,'original_frozen_head':prep['original_frozen_head'],'frozen_utc':t,'files':files}
(A/'scope_repaired_snapshot_manifest.json').write_text(json.dumps(out,indent=2)+'\n')
receipt={'utc':t,'pr':n,'repaired_head':commit,'parents':[old,main],'original_head':prep['original_frozen_head'],'changed_current_wrappers':changed,'new_current_files':added,'preserved_prior_target_files':len(preserved),'all_historical_author_and_review_bytes_unchanged':True,'all_current_paths':len(files),'queue_line':idx+1,'queue_cells':[8,9],'old_row':before.decode(),'new_row':lines[idx].decode(),'all_other_queue_bytes_preserved':True,'scope_snapshot_manifest':'scope_repaired_snapshot_manifest.json','nonforce_branch_push_confirmed':True,'recovered_after_transient_stale_PR_API_without_repeating_push':bool(resume),'workflow_percent':90,'fresh_corrected_head_gate_pending':True}
(A/'scope_branch_repair_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
inv=json.loads((P/'inventory.json').read_text());x=next(x for x in inv['items'] if x['number']==n);x.update(current_review_head=commit,disposition='scope_repaired_fresh_final_review_pending',audit_workflow_percent=90);(P/'inventory.json').write_text(json.dumps(inv,indent=2)+'\n')
for f in [P/'RESEARCH_LOG.md',A/'README.md']:
 with f.open('a') as h:h.write(f'\n{t}: PR{n} scope correction `{commit}` globally bound in current wrappers; {len(preserved)} prior target files unchanged, two additive correction files, queue own line{idx+1} cells8/9 only against main{main}. Workflow90%, original resolution0%; new corrected-head adversary pending.\n')
print(json.dumps(receipt,indent=2))
