"""Preserve the initial unreviewed plan and add authored audit-custody records.

No manuscript, public deposit, tracker, native file or Git mutation occurs.
The corrected plan still requires ROOT review, a final ACK and actual-window gate.
"""
import datetime, hashlib, json, os, stat, sys
from pathlib import Path

if sys.flags.optimize:
    raise RuntimeError('Optimization disables validation')
R = Path('/Users/alec/Documents/Math')
A = R/'draft_pr_publication_program_20260930/audits/pr80_30000177'
path = A/'ROOT_NATIVE_PLAN_PREPARED_20261004.json'
initial = path.read_bytes()
plan = json.loads(initial)
assert plan['ROOT_reviewed_for_execution'] is False
assert plan['PR']==80 and plan['DOI']=='10.5281/zenodo.23147866'
preserved = A/'ROOT_NATIVE_PLAN_INITIAL_UNREVIEWED_20261004.json'
with preserved.open('xb') as stream:
    stream.write(initial)

def pin(p):
    assert p.is_file() and not p.is_symlink() and p.resolve()==p
    b = p.read_bytes()
    return {'path':str(p.relative_to(R)), 'bytes':len(b),
            'sha256':hashlib.sha256(b).hexdigest(),'mode':stat.S_IMODE(p.stat().st_mode)}

added = []
for name in ('target_priority_family_20261004','mechanism_priority_family_20261004',
             'priority_gate_adjudicator_20261004','whole_preprint_round1_20261004'):
    for p in sorted((A/name).iterdir()):
        # These top-level files are authored audit reports, custody manifests,
        # scope/first assessments and code. Raw fetched responses are excluded.
        if not p.is_file() or p.suffix not in ('.md','.py','.json') or p.name.startswith('web_'):
            continue
        entry = pin(p)
        if entry['path'] not in plan['checkpoint_files']:
            plan['checkpoint_files'][entry['path']] = entry
            plan['bound_inputs'].append(entry)
            added.append(entry)
self_pin = pin(Path(__file__).resolve())
plan['checkpoint_files'][self_pin['path']] = self_pin
plan['bound_inputs'].append(self_pin)
plan['exact_owned_paths'] = sorted(set(plan['exact_owned_paths'])|set(plan['checkpoint_files']))
plan['UTC'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
plan['status'] = 'CORRECTED_CONCRETE_PLAN_AWAITING_ROOT_AND_OPERATIONAL_READBACK'
plan['checkpoint_selection_correction'] = {
    'ROOT_origin_lead_after_operational_initial_FIRST':True,
    'initial_plan':pin(preserved),'added_authored_file_count':len(added),
    'paper_payloads_and_metadata_changed':False,'native_operator_changed':False,
    'new_writer_authority':False}
path.write_text(json.dumps(plan,indent=2)+'\n')
receipt = {'UTC':plan['UTC'],'actual_PID':os.getpid(),
           'initial_plan':pin(preserved),'corrected_plan':pin(path),
           'initial_checkpoint_count':len(json.loads(initial)['checkpoint_files']),
           'corrected_checkpoint_count':len(plan['checkpoint_files']),
           'added_authored_records':added,'revision_source':self_pin,
           'ROOT_origin_lead_after_operational_initial_FIRST':True,
           'published_payloads_unchanged':True,'native_or_Git_mutation':False,
           'ROOT_reviewed_for_execution':False}
with (A/'ROOT_NATIVE_CHECKPOINT_SELECTION_REPAIR_20261005.json').open('x') as stream:
    stream.write(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({key:receipt[key] for key in ('initial_checkpoint_count','corrected_checkpoint_count','corrected_plan','ROOT_reviewed_for_execution')},indent=2))
