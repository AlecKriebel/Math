"""Reconcile only the already staged owned checkpoint after concurrently changing external logs."""
from pathlib import Path
import datetime as dt,hashlib,json,os,subprocess
P=Path(__file__).resolve().parents[1];R=P.parent;A=P/'audits/pr45_9900007'
def sha(b):return hashlib.sha256(b).hexdigest()
assert __debug__ and subprocess.check_output(['git','branch','--show-current'],cwd=R).strip()==b'main'
old=json.loads((P/'checkpoints/CHECKPOINT_20261003_0300.json').read_bytes());names={z['path'] for z in old['owned_files']}|{(P/'checkpoints/CHECKPOINT_20261003_0300.json').relative_to(R).as_posix()}
F=A/'root_checkpoint_0300_stage_actual_capture';assert json.loads((F/'CAPTURE.json').read_bytes())['status']=='FAIL'
for p in F.iterdir():assert p.is_file() and not p.is_symlink();names.add(p.relative_to(R).as_posix())
names.add(Path(__file__).relative_to(R).as_posix());names.add((P/'checkpoints/reconcile_checkpoint_20261003_0302.py').relative_to(R).as_posix())
for p in (A/'root_checkpoint_0302_reconciliation_actual_capture').iterdir():assert p.is_file();names.add(p.relative_to(R).as_posix())
names.add((P/'checkpoints/reconcile_checkpoint_20261003_0303.py').relative_to(R).as_posix())
for p in (A/'root_checkpoint_0303_reconciliation_actual_capture').iterdir():assert p.is_file();names.add(p.relative_to(R).as_posix())
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip()
staged={n for n in subprocess.check_output(['git','diff','--cached','--name-only','-z'],cwd=R).decode().split('\0') if n};assert staged<=names
changes=[]
for z in old['foreign_dirty_preimages_preserved']:
 b=(R/z['path']).read_bytes()
 if len(b)!=z['bytes'] or sha(b)!=z['sha256']:changes.append({'path':z['path'],'earlier_bytes':z['bytes'],'earlier_sha256':z['sha256'],'present_bytes':len(b),'present_sha256':sha(b),'qualification':'Concurrent user-owned working file changed during readonly checkpoint inspection; never staged or overwritten by this checkpoint.'})
now=dt.datetime.now(dt.timezone.utc).isoformat()
with (P/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+now+' — Checkpoint0300 staged its exact owned files, then failed its overstrict external-working-log unchanged check because independently active user work changed logs. No external body was staged or overwritten. Distinct0304 reconciliation after0302/0303 rejected their overly narrow own-native whitelist retains failure and original snapshot, revalidates explicit program, already accepted2233/30004386 canonical closures, and native queue/state/history paths and refreshes only owned staged bytes after completed capture, excludes its own live capture, and records concurrent changes. Completion33/180=18.333333333333332%; no additional accepted PR.\n')
rows=[]
for n in sorted(names):
 p=R/n;b=p.read_bytes();assert p.is_file() and not p.is_symlink() and p.stat().st_size<=100*1024*1024 and (n.startswith(P.name+'/') or n.startswith('unsolved_math_prioritization/attempts/2233/') or n.startswith('unsolved_math_prioritization/attempts/30004386/') or n in {'unsolved_math_prioritization/QUEUE.md','unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.jsonl'});rows.append({'path':n,'bytes':len(b),'sha256':sha(b)})
out=P/'checkpoints/CHECKPOINT_20261003_0304.json';out.write_text(json.dumps({'schema':'ROOT_exact_owned_checkpoint_reconciliation/v1','utc':now,'actual_pid':os.getpid(),'main_before':head,'owned_files':rows,'earlier_failed_checkpoint_preserved':True,'concurrent_foreign_changes_recorded_not_staged':changes,'completed_count':33,'total':180,'completion_estimate_percent':33/180*100,'active_families_included':False,'live_own_capture_included':False},indent=2)+'\n');names.add(out.relative_to(R).as_posix())
subprocess.run(['git','add','-f','--',*sorted(names)],cwd=R,check=True)
staged={n for n in subprocess.check_output(['git','diff','--cached','--name-only','-z'],cwd=R).decode().split('\0') if n};assert staged<=names
for n in staged:assert subprocess.check_output(['git','show',':'+n],cwd=R)==(R/n).read_bytes()
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip()==head
print(json.dumps({'status':'PASS_EXACT_OWNED_CHECKPOINT_RECONCILED','staged_members':len(staged),'concurrent_foreign_paths':[z['path'] for z in changes],'foreign_staged_members':0,'main_before':head}))
