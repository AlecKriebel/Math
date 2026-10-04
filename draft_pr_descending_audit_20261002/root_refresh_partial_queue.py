"""Repair only a partial PR queue via scoped recursive trees; no private full index."""
import datetime, hashlib, json, os, subprocess, sys, uuid
from pathlib import Path
P=Path(__file__).resolve().parent;A=P/'audits'/sys.argv[1];n=int(sys.argv[2]);problem=sys.argv[3]
original=json.loads((A/'snapshot_manifest.json').read_text());frozen_original=original['head'];old=frozen_original
criteria=json.loads((A/'acceptance_criteria.json').read_text())
proposal=[criteria['accepted_status'],criteria['author_turns']]
assert proposal in (['unsolved','5/5'],['already_solved','0/5'],['already_solved','1/5'])
assert subprocess.check_output(['git','branch','--show-current']).strip()==b'main'
assert subprocess.run(['git','rev-parse','-q','--verify','MERGE_HEAD'],capture_output=True).returncode!=0
resolution=0 if proposal[0]=='unsolved' else 100
inv_initial=json.loads((P/'inventory.json').read_text())
branch=next(x['headRefName'] for x in inv_initial['items'] if x['number']==n)
queue='unsolved_math_prioritization/QUEUE.md'
def git(*args,input=None,env=None):return subprocess.check_output(['git',*args],input=input,env=env)
frozen_lines=git('show',f'{frozen_original}:{queue}').splitlines(keepends=True)
frozen_rows=[l for l in frozen_lines if len(l.split(b'|'))>9 and l.split(b'|')[2].strip().split(b' / ')[0].decode()==problem]
assert len(frozen_rows)==1
frozen_cells=frozen_rows[0].split(b'|')
assert [frozen_cells[j].strip().decode() for j in (8,9)]==proposal,'accepted root criteria disagree with original queue disposition'
def run(args,tag,ok=(0,)):
 r=subprocess.run(args,capture_output=True);(A/(tag+'.stdout')).write_bytes(r.stdout);(A/(tag+'.stderr')).write_bytes(r.stderr);assert r.returncode in ok,(tag,r.returncode,r.stderr.decode());return r
r=json.loads(run(['gh','pr','view',str(n),'--json','state,headRefOid,isDraft'],'repair_remote').stdout)
assert r['state']=='OPEN'
if r['headRefOid']!=frozen_original:
 prior=json.loads((A/'repaired_snapshot_manifest.json').read_text())
 assert r['headRefOid']==prior['head'] and prior['original_frozen_head']==frozen_original
 old=prior['head']
 assert set(git('diff','--name-only',prior['base'],old).decode().splitlines())=={e['path'] for e in original['files']}
 for e in original['files']:
  if e['path']!=queue:assert git('show',f"{old}:{e['path']}")==git('show',f"{frozen_original}:{e['path']}"),e['path']
 archive=A/'queue_refresh_history'/old;archive.mkdir(parents=True,exist_ok=False)
 for name in ['repaired_snapshot_manifest.json','queue_repair_receipt.json','root_exact_live_receipt.json']:
  if (A/name).exists():(archive/name).write_bytes((A/name).read_bytes())
 (A/'repaired_snapshot').rename(archive/'repaired_snapshot')
else:assert r['isDraft']
run(['git','fetch','origin','main'],'repair_main_fetch');main=git('rev-parse','origin/main').decode().strip()
v=run(['git','merge-tree','--write-tree',old,main],'repair_merge_tree',ok=(0,1));tree=v.stdout.decode().splitlines()[0]
if v.returncode:
 conflicts=[x.rsplit('\t',1)[1] for x in v.stdout.decode().splitlines() if '\t' in x]
 assert conflicts and set(conflicts)=={queue},conflicts
raw=git('show',f'{main}:{queue}');lines=raw.splitlines(keepends=True)
matches=[i for i,l in enumerate(lines) if len(l.split(b'|'))>9 and l.split(b'|')[2].strip().split(b' / ')[0].decode()==problem]
assert len(matches)==1;idx=matches[0];cells=lines[idx].split(b'|');assert cells[8].strip()==b'queued' and cells[9].strip()==b'0/5'
before=lines[idx];cells[8:10]=frozen_cells[8:10];lines[idx]=b'|'.join(cells);new=b''.join(lines)
changed_cells=[j for j,(x,y) in enumerate(zip(before.split(b'|'),cells)) if x!=y]
assert changed_cells==([8,9] if proposal[1]!='0/5' else [8])
def replace_blob(tree_oid,parts,blob_oid):
 rows=git("ls-tree","-z",tree_oid).split(b"\0");out=[];found=False
 for row in rows:
  if not row:continue
  meta,name=row.split(b"\t",1);mode,kind,oid=meta.split()
  if name.decode()==parts[0]:
   assert not found;found=True
   if len(parts)==1:
    assert mode==b"100644" and kind==b"blob";oid=blob_oid.encode()
   else:
    assert mode==b"040000" and kind==b"tree";oid=replace_blob(oid.decode(),parts[1:],blob_oid).encode()
  out.append(b" ".join([mode,kind,oid])+b"\t"+name+b"\0")
 assert found
 return git("mktree","-z",input=b"".join(out)).decode().strip()
blob=git("hash-object","-w","--stdin",input=new).decode().strip();tree=replace_blob(tree,queue.split("/"),blob)
paths=set(git('diff','--name-only',main,tree).decode().splitlines());expected={e['path'] for e in original['files']};assert paths==expected,(paths-expected,expected-paths)
for e in original['files']:
 if e['path']!=queue:assert git('show',f"{tree}:{e['path']}")==git('show',f"{old}:{e['path']}"),e['path']
commit=git('commit-tree',tree,'-p',old,'-p',main,input=f'Repair PR{n} queue against current accepted main; preserve all mathematical files\n'.encode()).decode().strip()
run(['git','push','origin',f'{commit}:refs/heads/{branch}'],'repair_push')
files=[];S=A/'repaired_snapshot'
for path in sorted(paths):
 b=git('show',f'{commit}:{path}');f=S/path;f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(b);files.append({'path':path,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
t=datetime.datetime.now(datetime.timezone.utc).isoformat();manifest={'pr':n,'head':commit,'base':main,'original_frozen_head':frozen_original,'previous_review_head':old,'frozen_utc':t,'files':files};(A/'repaired_snapshot_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
receipt={'utc':t,'pr':n,'original_head':frozen_original,'previous_review_head':old,'repaired_head':commit,'current_main_parent':main,'parents':[old,main],'tree':tree,'all_original_target_files_unchanged':len(paths)-1,'changed_queue_line':idx+1,'changed_queue_pipe_cells':changed_cells,'accepted_status':proposal[0],'author_turns':proposal[1],'old_row':before.decode(),'new_row':lines[idx].decode(),'all_other_queue_bytes_preserved':True,'nonforce_branch_push_succeeded':True,'raw_source_count':0}
(A/'queue_repair_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
inv=json.loads((P/'inventory.json').read_text());x=next(x for x in inv['items'] if x['number']==n);x.update(original_frozen_head=frozen_original,current_review_head=commit,disposition='queue_repaired_fresh_whole_package_review_pending',audit_workflow_percent=90);(P/'inventory.json').write_text(json.dumps(inv,indent=2)+'\n')
for f in [P/'RESEARCH_LOG.md',A/'README.md']:
 with f.open('a') as h:h.write(f'\n{t}: PR{n} queue-only repair `{commit}` against actual main `{main}`; all{len(paths)-1} target bytes unchanged, only own queue line{idx+1} cells{changed_cells}. Status{proposal[0]},{proposal[1]}; workflow90%, original resolution{resolution}% (credited prior literature when already_solved); fresh exact-head final audit pending.\n')
print(json.dumps(receipt,indent=2))
