"""Prepare a concrete scoped checkpoint plan without changing shared tracked files/index."""
from pathlib import Path
import datetime,hashlib,json,os,subprocess
A=Path(__file__).resolve().parent;P=A.parent.parent;C=P.parent
G='/opt/homebrew/Cellar/git/2.38.2/bin/git'
def req(ok,msg):
 if not ok:raise RuntimeError(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def run(args):
 r=subprocess.run([G,*args],cwd=C,capture_output=True)
 req(r.returncode==0,'Read-only Git probe failed')
 return r.stdout
target=A/'MATH_PRIORITY_CHECKPOINT_PLAN_20261006.json'
req(not target.exists(),'Existing prepared plan; inspect before retry')
gate=json.loads((A/'ROOT_PRIORITY_GATE_20261006.json').read_text())
req(gate['mathematical_and_source_status']=='PASS' and not gate['publication_clearance'],'Current withheld priority gate')
req(not run(['diff','--cached','--name-only']) and not run(['diff','--name-only','--diff-filter=ACMRTUXB']),'Shared index/materialized tracked edit observed; no plan until coordinated')
raw=run(['ls-files','--others','--exclude-standard','-z','--',str(A.relative_to(C))]).decode().split('\0')
sealed_public={str((A/x['path']).relative_to(C)) for x in json.loads((A/'ROOT_PRIORITY_FAMILY_AUTHENTICATION_20261006.json').read_text())['mathematical47_members_unchanged']}
members=[]
for s in sorted(x for x in raw if x):
 p=C/s;r=p.relative_to(A)
 req(p.is_file() and not p.is_symlink(),'Owned regular file')
 req(not {'private_sources','__pycache__'}.intersection(r.parts),'Private member rejected')
 if 'runs' in r.parts:req(s in sealed_public,'Only authenticated sealed public run receipts may be selected')
 req(p.suffix.lower() not in {'.pdf','.png','.jpg','.html','.sqlite3','.zip'},'Private/binary source rejected')
 b=p.read_bytes();members.append({'path':s,'bytes':len(b),'sha256':sha(b)})
record={'schema':'pr124-concrete-root-math-priority-checkpoint-plan/v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_preparer_PID':os.getpid(),'observed_main':run(['rev-parse','HEAD']).decode().strip(),'owned_new_public_members':members,'owned_new_public_member_count':len(members),'planned_tracked_updates':[str((P/n).relative_to(C)) for n in ['CURRENT_PROGRESS.json','CURRENT_PROGRESS.md','RESEARCH_LOG.md']]+[str((A/'RESEARCH_LOG.md').relative_to(C))],'tracked_update_intent':'Math/sourcePASS100%; all bounded priority families complete; application novelty unresolved with material book gap, source access question pending; workflow35%, publication0; completion20/99 and11 published; correct late117 receipt commit6ca without self-commit claim. Preserve all unrelated bodies and index.','future_operational_members':['checkpoint_math_priority_root_20261006.py','MATH_PRIORITY_WRITER_HANDOFF_20261006.json','MATH_PRIORITY_WRITER_REQUEST_API_RESPONSE_20261006.json','MATH_PRIORITY_CHECKPOINT_SELECTION_20261006.json'],'late_previous_receipts_selected':True,'private_source_PDF_text_images_excluded':True,'active_agent_folders_selected':False,'native_PR_Zenodo_Sheet_mutations_planned':False,'writer_currently_released':True,'fresh_explicit_writer_handoff_required':True,'global_tracked_files_updated':False,'index_changed':False,'goal_active':True}
target.write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
print(json.dumps({'UTC':record['UTC'],'PID':os.getpid(),'owned_new_public_members':len(members),'planned_tracked_updates':4,'observed_main':record['observed_main'],'shared_mutations':False}))
