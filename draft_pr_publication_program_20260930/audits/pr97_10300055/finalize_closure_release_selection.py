"""Keep current goal-state metadata faithful to the last actual tool status."""
from pathlib import Path
import datetime, hashlib, json, os
A=Path(__file__).resolve().parent
P=A.parents[1]
C=P.parent
progress_path=P/'CURRENT_PROGRESS.json'
progress=json.loads(progress_path.read_text())
if progress['current_PR']!=97 or not progress['current_closed_without_merging']:
    raise RuntimeError('Closure handoff changed')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
progress.update({'UTC':now,'updated_UTC':now,'persistent_goal_status':'blocked',
                 'current_previous_goal_blocker_resolved':True,
                 'current_goal_publication_permission_gate_unresolved':False,
                 'next_step':'Fresh ordered intake after97 on goal resumption; no PR97 publication decision remains pending.'})
progress_path.write_text(json.dumps(progress,indent=2)+'\n')
with (A/'RESEARCH_LOG.md').open('a') as stream:
    stream.write('\n### '+now+' — closure handoff goal-state alias reconciled\n'
                 'The scheduler was actually last read as blocked; corrected the stale active metadata alias. Its former PR97 disposition gate is resolved by the verified human-directed closure, and no further PR97 publication choice is pending. The scheduler cannot be resumed through update_goal. Next ordered intake remains after97 when the goal resumes. Completion estimates unchanged: PR97workflow100%;14/99=14.14%. No mathematical, native-status, frozen-paper or service changes.\n')
old=json.loads((A/'CLOSURE_RELEASE_SELECTION_20261006.json').read_text())
selected={C/rel for rel in old['paths']}
selected.update([Path(__file__).resolve(),A/'CLOSURE_RELEASE_SELECTION_20261006.json'])
selected.update(p for p in (A/'actual_operations/record_closure_completion').glob('*') if p.is_file() and not p.is_symlink())
rows=[]
for p in sorted(selected):
    if not p.is_file() or p.is_symlink() or not p.resolve().is_relative_to(C.resolve()):raise RuntimeError('Unsafe selected body')
    b=p.read_bytes();rows.append({'path':p.relative_to(C).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
out={**old,'UTC':now,'operator_PID':os.getpid(),'paths':[r['path'] for r in rows],'pins':rows}
with (A/'CLOSURE_RELEASE_FINAL_SELECTION_20261006.json').open('x') as stream:
    stream.write(json.dumps(out,indent=2)+'\n')
print(json.dumps({'UTC':now,'operator_PID':os.getpid(),'files':len(rows),'bytes':sum(r['bytes'] for r in rows),
                  'PR97_closed':True,'disposition_question_pending':False}))
