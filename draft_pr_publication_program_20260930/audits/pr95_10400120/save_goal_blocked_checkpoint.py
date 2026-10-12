from pathlib import Path
import datetime, hashlib, json, os
A=Path(__file__).resolve().parent
C=A.parents[2]
P=A.parents[1]
utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
tool=json.loads((A/'ROOT_PERSISTENT_GOAL_BLOCKED_TOOL_RESULT_20261005.json').read_text())
if tool['goal']['status']!='blocked': raise RuntimeError('blocked tool outcome not confirmed')
audit=json.loads((A/'ROOT_PERSISTENT_GOAL_BLOCKED_AUDIT_20261005.json').read_text())
if not audit['blocked_audit_passed'] or audit['consecutive_goal_turns_with_same_blocking_condition']<3: raise RuntimeError('blocked threshold not met')
def pin(f):
    b=f.read_bytes()
    return {'file':str(f.relative_to(P)), 'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
status={'schema':'persistent-goal-actual-blocked-status/v1','UTC':utc,'actual_operator_PID':os.getpid(),'status':'blocked','goal_complete':False,'PR':95,'mathematical_result_verified':True,'priority_requirement_complete':False,'blocking_condition_unchanged':True,'needed_input':audit['needed_external_change'],'program_completed_dispositions':12,'dated_eligible_total':99,'program_workflow_estimate_percent':12/99*100,'PR95_workflow_estimate_percent':45,'mathematical_audit_percent':100,'priority_workflow_estimate_percent':85,'inputs':[pin(A/'ROOT_PERSISTENT_GOAL_BLOCKED_AUDIT_20261005.json'),pin(A/'ROOT_PERSISTENT_GOAL_BLOCKED_TOOL_RESULT_20261005.json')],'historical_pending_goal_status_note_superseded':True,'no_further_scientific_or_service_work_after_status_change':True}
(A/'ROOT_PERSISTENT_GOAL_BLOCKED_STATUS_20261005.json').write_text(json.dumps(status,indent=2)+'\n')
progress=json.loads((P/'CURRENT_PROGRESS.json').read_text())
progress['UTC']=utc
progress['persistent_goal_status']='blocked'
progress['persistent_goal_blocked_actual_record']='audits/pr95_10400120/ROOT_PERSISTENT_GOAL_BLOCKED_STATUS_20261005.json'
progress['remaining_current_step']='Resume when legitimate full Kuriya GP-preprint text or materially new primary scope evidence becomes available. Priority requirement remains unresolved; mathematics verified. No publication, merge or ordered advance. Persistent goal blocked after three consecutive turns with the same condition.'
(P/'CURRENT_PROGRESS.json').write_text(json.dumps(progress,indent=2)+'\n')
with (A/'PRIORITY_STATUS.md').open('a') as f:
    f.write('\nAt '+utc+', the persistent goal was set to blocked by the actual goal tool after the same source condition recurred in three consecutive goal turns. Fresh GitHub metadata confirms PR95 remains an open draft at the reviewed immutable head, and both new source agents are terminal. The prior turn made concrete progress; all current bounded trails are now closed. This status supersedes the earlier active-goal snapshot without changing the verified mathematical result or establishing priority. A legitimate complete Kuriya text or materially new primary scope evidence is required to resume the priority gate. No PR95 publication, merge or ordered advance occurred.\n')
with (A/'RESEARCH_LOG.md').open('a') as f:
    f.write('\n### '+utc+' — actual persistent-goal blocked checkpoint; PR95 workflow 45%, mathematics 100%, priority workflow 85%; program 12/99 (12.12%)\nPrevious goal turn classified as progress: 5008d0b3d1f4e96d747ca395611450651cef0e0f is confirmed on local and remote main and its actual recorder completed with exit 0. Fresh native metadata confirms the exact reviewed PR95 head remains open/draft; literal claimed_solved status was re-read from the correct Git QUEUE path. Both source agents are terminal. The same unavailable Kuriya priority source has now persisted for three consecutive goal turns; available bounded trails are closed and no live process is awaited. The actual goal tool returned blocked, preserved in the adjacent tool-result/status records. No scientific, publication, PR, tracker, UI, outreach, cleanup or shared-checkout work follows that status change; this checkpoint saves the control evidence only. Full goal remains incomplete.\n')
files=[P/'CURRENT_PROGRESS.json']+[A/n for n in ['PRIORITY_STATUS.md','RESEARCH_LOG.md','record_priority_blocked_audit.py','save_goal_blocked_checkpoint.py','ROOT_PERSISTENT_GOAL_BLOCKED_AUDIT_20261005.json','ROOT_PERSISTENT_GOAL_BLOCKED_TOOL_RESULT_20261005.json','ROOT_PERSISTENT_GOAL_BLOCKED_STATUS_20261005.json']]
for op in ['checkpoint_priority_followup','blocked_audit_PR95_native_snapshot','root_priority_blocked_audit']:
    files += [f for f in (A/'actual_operations'/op).iterdir() if f.is_file()]
files += [A/'actual_checkpoints/closed_priority_followup/RECEIPT.json',A/'actual_checkpoints/closed_priority_followup/PROCESS_JOURNAL.json']
files=sorted(set(files))
plan={'UTC':utc,'actual_operator_PID':os.getpid(),'paths':[str(f.relative_to(C)) for f in files],'pins':[{'file':str(f.relative_to(C)),'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()} for f in files],'scope':'Actual blocked audit/status and checkpoint receipts only. No raw research source files or primary checkout/index mutation.','branch':'main','goal_status':'blocked'}
dest=A/'BLOCKED_STATUS_CHECKPOINT_SELECTION_20261005.json'
plan['paths'].append(str(dest.relative_to(C)))
dest.write_text(json.dumps(plan,indent=2)+'\n')
print(json.dumps({'UTC':utc,'actual_operator_PID':os.getpid(),'actual_goal_status':'blocked','selected_files':len(plan['paths'])}))
