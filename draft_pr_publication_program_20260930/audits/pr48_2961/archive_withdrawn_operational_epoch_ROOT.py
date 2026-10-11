"""Move ROOT's withdrawn operational epoch intact; no native or Git mutations."""
from pathlib import Path
import datetime,hashlib,json,os,stat,subprocess
R=Path('/Users/alec/Documents/Math');A=R/'draft_pr_publication_program_20260930/audits/pr48_2961'
names=['ROOT_SOURCE_ACCEPTANCE_REVIEW.json','ROOT_IMMUTABLE_ACCEPTANCE_BINDINGS.json','ROOT_FINAL_PLAN.json','ROOT_FRESH_ACCEPTANCE_INPUT_PREIMAGES.json','root_acceptance_author_readonly_inputs','root_final_reconciliation_actual_capture','root_final_reconciled','root_preflight_actual_capture','integration_preflight.json','integration_queue_before.md','integration_state_before.json','integration_history_before.jsonl','integration_inventory_before.json','accepted_pr_body.md']
def sha(b):return hashlib.sha256(b).hexdigest()
def snapshot(p):
 rows=[]
 for q in [p,*sorted(p.rglob('*'))] if p.is_dir() else [p]:
  s=q.lstat();assert not q.is_symlink() and (stat.S_ISREG(s.st_mode) or stat.S_ISDIR(s.st_mode))
  z=dict(path=q.relative_to(A).as_posix(),full_mode=stat.S_IMODE(s.st_mode),type='dir' if q.is_dir() else 'file')
  if q.is_file():b=q.read_bytes();z.update(bytes=len(b),sha256=sha(b))
  rows.append(z)
 return rows
cap=json.loads((A.parent/'pr45_9900007/root_pr48_withdraw_unfinished_merge_actual_capture/CAPTURE.json').read_bytes())
assert cap['status']=='PASS' and cap['pid']==67296 and cap['exit_code']==0
result=json.loads((A/'withdrawn_unfinished_merge_20261003_1212/RESULT.json').read_bytes())
assert result['status']=='PASS_WITHDRAWN_OWNED_UNFINISHED_MERGE_FOREIGN_STAGING_PRESERVED'
assert not (R/'.git/MERGE_HEAD').exists() and not (A/'root_overlay_actual_capture').exists() and not (A/'integration_check.json').exists()
fresh=json.loads((A/'ROOT_FRESH_ACCEPTANCE_INPUT_PREIMAGES.json').read_bytes())
native=[]
for z in fresh['files']:
 p=R/z['path'];b=p.read_bytes();s=p.stat();assert len(b)==z['bytes'] and sha(b)==z['sha256'] and stat.S_IMODE(s.st_mode)==z['worktree_mode']
 native.append((str(p),b,stat.S_IMODE(s.st_mode)))
assert len(names)==14 and len(set(names))==14
before=[]
for n in names:assert (A/n).exists();before.extend(snapshot(A/n))
D=A/'historical_operational_epoch_20261003_1143_withdrawn';D.mkdir(exist_ok=False)
for n in names:os.rename(str(A/n),str(D/n))
after=[]
for n in names:
 for z in snapshot(D/n):z['path']=z['path'].removeprefix(D.name+'/');after.append(z)
assert before==after and all(not (A/n).exists() for n in names)
for n,b,m in native:p=Path(n);assert p.read_bytes()==b and stat.S_IMODE(p.stat().st_mode)==m
record=dict(schema='pr48-withdrawn-operational-epoch-qualification/v1',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),actual_archiver_pid=os.getpid(),historical_author_pid=45178,historical_sealer_pid=46948,historical_preflight_pid=47114,historical_ready_pid=48289,historical_body_pid=49084,historical_merge_pid=49087,failed_overlay_outer_pid=50550,owned_merge_withdrawal_pid=67296,original_paths_prefix='draft_pr_publication_program_20260930/audits/pr48_2961/',retained_paths_prefix=D.relative_to(R).as_posix()+'/',exact_members_with_original_relative_paths=before,body_full_mode_and_topology_preserved=True,native13_unchanged=True,Git_index_refs_remote_untouched=True,reason='Unrelated main and foreign staged/worktree bodies advanced after the real preflight; no overlay child was launched. ROOT withdrew only its original unfinished merge and preserved all foreign staging. These valid dated operational records do not authorize a future live epoch. A new genuine ROOT fresh author, sealer and all six actual phases are required; the closed mathematical and SOURCE reviews remain unchanged.',acceptance_completed=False)
with (D/'EPOCH_QUALIFICATION.json').open('xb') as f:f.write((json.dumps(record,indent=2)+'\n').encode())
print(json.dumps(dict(status='PASS_WITHDRAWN_OPERATIONAL_EPOCH_PRESERVED',items=len(names),members=len(before),archive=D.relative_to(R).as_posix(),native13_unchanged=True,acceptance_completed=False)))
