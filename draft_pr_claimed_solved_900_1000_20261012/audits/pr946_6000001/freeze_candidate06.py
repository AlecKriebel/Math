"""Freeze a repaired candidate06 and run actual read-only readiness gates."""
import sys
if not sys.flags.isolated or sys.flags.optimize:
    raise RuntimeError('Use Python -I -B without optimization')
from pathlib import Path
import datetime, hashlib, json, os, types

ROOT = Path('/Users/alec/Documents/Math')
P = ROOT / 'draft_pr_claimed_solved_900_1000_20261012'
A = P / 'audits/pr946_6000001'
D = A / 'preprint'
CORE = '8e1a0d7b3ca6e5d72e76415541b393fbfbe52e307368bc86b9e7982d5be27cd7'

def fp(path):
    raw = path.read_bytes()
    return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}

def obj(path):
    return json.loads(path.read_bytes())

def save_new(path, value):
    with path.open('x') as handle:
        json.dump(value,handle,indent=2)
        handle.write('\n')

core = P/'accept_pr946.py'
if fp(core)['sha256'] != CORE:
    raise RuntimeError('Externally tested candidate06 core differs')
old = obj(D/'reviewed_candidates/candidate05/FREEZE.json')
if obj(D/'FREEZE.json') != old:
    raise RuntimeError('Expected unchanged candidate05 freeze before revision')
controls = obj(A/'REVIEW05_GLOBAL_CLOSURE_CONTROLS.json')
if not (controls['status'] == 'PASS' and controls['root_control_count'] == 105
        and controls['subject_core_sha256'] == CORE and controls['actual_external_mutations'] == 0):
    raise RuntimeError('Complete root105 repair controls required')
now = datetime.datetime.now(datetime.timezone.utc).isoformat()
save_new(A/'REVIEW05_REPAIR_RESOLUTIONS.json', {
    'utc':now,'pr':946,'status':'ROOT_REPAIRED_PENDING_NEW_ENTIRE_FULL_REVIEW06',
    'required_and_residual_issues':['FP05-OPS-001','FP05-OPS-002','FP02-OPS-001'],
    'repair':'Factor candidate_state_check; repeat current candidate/dependency authentication and sealed review/historical-candidate closure immediately before initial exclusive approval save. At every existing shared action boundary, after full source/review reads and current canonical-state refresh, reauthenticate externally sealed review contents and complete historical frozen contexts with no intervening Git/service call. All earlier guards remain.',
    'independent_old_defects_reproduced':{'receipt':'ROOT_REVIEW05_OLD_DEFECT_REPRODUCTION.json','cases':82},
    'actual_directory_and_global_fake_service_controls':{'receipt':'REVIEW05_GLOBAL_CLOSURE_CONTROLS.json','cases':105,
        'new_root_cases':'Nine final actual-source acceptance closure classes, restored full chain, valid initial approval/readback, and twelve full-service positive/negative cases.',
        'fixture':'Complete immutable candidate05 transport inventory, actual real01..04 sealed historical reports/contexts, explicitly synthetic terminal05; new subject tested separately. Actual current06 context is independently gated below and must be tested by NEW06.'},
    'earlier_component_adapters':'All old dated84/68/17/11 fixtures remain unchanged with their original disclosed mocks; their green outputs are not evidence for the new current-state or sealed-closure guards. Root105 instead exercises actual relevant guard/approval/service paths.',
    'all_candidate05_files_and7sources_preserved':True,
    'paper_tex_pdf_inner_package_zip_outer_manifest_all223_payloads_byte_identical':True,
    'no_OS_atomic_hostile_filesystem_guarantee':True,'new_proof_responses':0,'external_mutations':0})
new_evidence = [
    'prepare_candidate06.py','apply_candidate06.py','freeze_candidate06.py','ROOT_FULL_REVIEW_05_VERIFICATION.json',
    'CANDIDATE05_PRESERVATION.json','REVIEW05_REPAIR_RESOLUTIONS.json',
    'REVIEW05_CLOSURE_CONTROLS.py','REVIEW05_GLOBAL_CLOSURE_CONTROLS.py',
    'ROOT_REVIEW05_OLD_DEFECT_REPRODUCTION.json','REVIEW05_GLOBAL_CLOSURE_CONTROLS.json',
    'ROOT_CANDIDATE06_CHANGE_SCOPE.json','OPERATIONS_CURRENT06_GUIDE.md']
freeze = json.loads(json.dumps(old))
freeze.update(utc=now,revision_candidate=6,
              operations_inventory_sha256=fp(A/'OPERATIONS_INVENTORY.json')['sha256'],
              readiness='FROZEN_CANDIDATE_ONLY; NEW06 entire independent full-package review remains outstanding')
freeze['future_helpers']['accept_pr946.py'] = fp(core)
for relative in new_evidence:
    path = A/relative
    freeze['evidence_files'][path.relative_to(ROOT).as_posix()] = fp(path)
temporary = D/'FREEZE.json.root-tmp'
temporary.write_text(json.dumps(freeze,indent=2)+'\n')
os.replace(temporary,D/'FREEZE.json')
pin = fp(D/'FREEZE.json')['sha256']
N = {'__name__':'_root_candidate06_readonly_','__file__':str(core)}
exec(compile(core.read_bytes(),str(core),'exec',dont_inherit=True,optimize=0),N)
context = N['capture_inventory'](freeze['operations_inventory_sha256'])
checked = N['freeze_check'](N['read_regular'](D/'FREEZE.json'),pin,context)
N['disposition_check']()
pr,parent,source,originals = N['premerge_gate'](checked,require_draft=True)
archive = N['archive_check'](checked,originals)
for number in range(1,6):
    base = D/'reviewed_candidates'/('candidate%02d'%number)
    raw = N['read_regular'](base/'FREEZE.json')
    N['freeze_check'](raw,N['sha'](raw),context,base=base,historical=True)
kit_key = 'zenodo_deposit_tool/zenodo.py'
kit = {'__name__':'_root_captured_kit_check6_','__file__':str(ROOT/kit_key)}
exec(compile(context['captured'][kit_key],str(ROOT/kit_key),'exec',dont_inherit=True,optimize=0),kit)
summary = kit['run'](types.SimpleNamespace(command='check',manifest=D/'zenodo-deposit.json',sandbox=False))
save_new(A/'ROOT_ZENODO_CANDIDATE06_LOCAL_CHECK.json',summary)
pr.pop('body',None)
save_new(A/'ROOT_CANDIDATE06_PRE_REVIEW_GATE.json', {
    'utc':N['utc_now'](),'result':'PASS_READONLY_PREPARATION_GATES','candidate_revision':6,
    'freeze_sha256':pin,'operations_inventory_sha256':context['inventory_sha256'],
    'actual_live_PR':pr,'fresh_main':parent,'source_gate':source,
    'all33_actual_Git_disk_archive_verified':True,'archive':archive,'captured_kit_local_check':'PASS',
    'historical_candidate01_02_03_04_05_authentication':'PASS',
    'FP05_and_residual_FP02_findings_repaired_pending_NEW_entire_full_review06':True,
    'all223_submission_payloads_byte_identical_to_candidate05':checked['files']==old['files'],
    'actual_external_mutations':0,'acceptance_merge_publication_tracker_native_actions_executed':False})
print(json.dumps({'status':'FROZEN6_AND_ACTUAL_PRE_REVIEW_GATES_PASS','freeze_sha256':pin,
                  'operations_inventory_sha256':context['inventory_sha256'],
                  'frozen_files':len(freeze['files']),'immutable_evidence':len(freeze['evidence_files']),
                  'fresh_main':parent,'actual_external_mutations':0}))
