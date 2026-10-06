"""Reconcile live workflow labels with the accepted frozen review and pending choice."""
from pathlib import Path
import datetime, hashlib, json, os, subprocess
A=Path(__file__).resolve().parent
P=A.parents[1]
C=P.parent
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
verdict=json.loads((A/'whole_package_round2_20261006/VERDICT.json').read_text())
readback=json.loads((A/'ROOT_ROUND2_CHECKPOINT_ACTUAL_READBACK_20261006.json').read_text())
if not verdict['whole_package_acceptance'] or verdict['issues'] or readback['human_answer_received']:
    raise RuntimeError('Disposition premises changed')
progress_path=P/'CURRENT_PROGRESS.json'
progress=json.loads(progress_path.read_text())
if progress['current_PR']!=97 or progress['current_publication_authorization']:
    raise RuntimeError('Current cursor/disposition changed')
progress.update({'UTC':now,'updated_UTC':now,
    'current_package_repair_status':'closed_corrected_fresh_round2_accepted',
    'next_step':'Await the already-delivered PR97-specific human disposition; original novelty clearance is not established.',
    'current_human_disposition_question_pending':True,
    'current_latest_completed_audit_checkpoint':'250d2043167ac97adedef188edd3aa7a1e938f85'})
progress_path.write_text(json.dumps(progress,indent=2)+'\n')
with (A/'RESEARCH_LOG.md').open('a') as stream:
    stream.write('\n### '+now+' — pending disposition handoff consistency\n'
      'Previous goal turn made progress by pushing and verifying the accepted qualified review checkpoint250d2043 and delivering the concrete PR97 disposition question. No human reply has arrived in this continuation. Original goal and current local state reread; live PR97 remains OPENdraft at fb50facb2a7389bb272bbf0b5cbd80c24c79b992. The obsolete repair-status label still said fresh review pending despite accepted Round2; corrected this current workflow label and next-step wording against the frozen verdict, without editing any frozen evidence or manuscript. Required choice remains unresolved for a second consecutive goal turn: publish qualified note, merge without paper, or hold for more priority evidence. The original novelty publication gate still applies; no service/merge/native action or next intake. PR97workflow60%; program13/99=13.13%; author2/5, extra proof-search0. No process wait is claimed.\n')
selected={progress_path,A/'RESEARCH_LOG.md',Path(__file__).resolve(),
          A/'ROOT_ROUND2_CHECKPOINT_ACTUAL_READBACK_20261006.json',
          A/'record_round2_checkpoint_readback.py',
          A/'ROUND2_ADJUDICATION_CHECKPOINT_RETRY_SELECTION.json',
          A/'actual_checkpoints/round2_adjudication_retry/RECEIPT.json',
          A/'actual_checkpoints/round2_adjudication_retry/PROCESS_JOURNAL.json'}
for folder in ['record_round2_checkpoint_readback','prepare_round2_checkpoint_retry','checkpoint_round2_adjudication_retry']:
    selected.update(p for p in (A/'actual_operations'/folder).glob('*') if p.is_file() and not p.is_symlink())
rows=[]
for p in sorted(selected):
    if not p.is_file() or p.is_symlink() or not p.resolve().is_relative_to(C.resolve()):
        raise RuntimeError('Unsafe path')
    b=p.read_bytes();rows.append({'path':p.relative_to(C).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
selection={'schema':'pr97-disposition-handoff-selection/v1','UTC':now,'operator_PID':os.getpid(),
           'expected_main':'250d2043167ac97adedef188edd3aa7a1e938f85','paths':[r['path'] for r in rows],
           'pins':rows,'human_reply_received':False,'publication_authorized':False,
           'blocked_condition_consecutive_goal_turns':2}
with (A/'DISPOSITION_HANDOFF_SELECTION_20261006.json').open('x') as stream:
    stream.write(json.dumps(selection,indent=2)+'\n')
print(json.dumps({'UTC':now,'operator_PID':os.getpid(),'files':len(rows),'bytes':sum(r['bytes'] for r in rows),
                  'human_disposition_pending':True}))
