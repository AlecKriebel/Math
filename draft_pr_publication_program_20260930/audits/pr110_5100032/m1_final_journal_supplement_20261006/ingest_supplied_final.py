"""Pin a user-supplied private journal source without redistributing its body."""
from pathlib import Path
import datetime, hashlib, json, os, shutil
D = Path(__file__).resolve().parent
S = D / 'private_sources'
S.mkdir(exist_ok=True)
original = Path('/Users/alec/Downloads/garcia2022.pdf')
b = original.read_bytes()
if not b.startswith(b'%PDF-'):
    raise RuntimeError('Not a PDF')
target = S / 'GKR_journal_final_2022.pdf'
if target.exists() and target.read_bytes() != b:
    raise RuntimeError('Source collision')
shutil.copyfile(original, target)
assert target.read_bytes() == b
r = {'schema':'pr110-supplied-M1-final-source/v1',
     'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),
     'actual_operator_PID':os.getpid(), 'original_path':str(original),
     'private_source':str(target.relative_to(D)), 'bytes':len(b),
     'sha256':hashlib.sha256(b).hexdigest(), 'redistributed':False,
     'required_doi':'10.1007/s10883-022-09608-y',
     'identity_and_full_body_comparison_pending':True,
     'goal_resumed_with_materially_new_source':True,
     'previous_blocker_turn_count_reset_for_resumed_run':True,
     'workflow_percent':30,'publication_percent':0}
(D/'SOURCE_INGESTION.json').write_text(json.dumps(r,indent=2)+'\n')
(D/'RESEARCH_LOG.md').write_text(r['UTC']+' — User supplied complete-looking journal PDF; actual11-page metadata matches required title/DOI. Private source pinned; full body and priority comparison pending. Workflow30%, publication0%.\n')
print(json.dumps(r))
