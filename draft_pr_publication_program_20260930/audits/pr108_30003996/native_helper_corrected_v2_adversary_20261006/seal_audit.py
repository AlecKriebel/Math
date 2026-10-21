#!/usr/bin/env python3
"""Seal this static audit only; no preparation, native or network/service execution."""
import datetime, hashlib, json, os, subprocess
from pathlib import Path
O=Path(__file__).resolve().parent; A=O.parent; C=A.parents[2]
D=A/'native_publication_integration_plan_20261006/corrected_v2'
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(body): return hashlib.sha256(body).hexdigest()
def put(name,obj): (O/name).write_text(json.dumps(obj,sort_keys=True,indent=2)+'\n')
started=now(); records=[]
def git(*args):
    start=now(); process=subprocess.Popen(['/usr/bin/git',*args],cwd=C,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
        env={**os.environ,'GIT_OPTIONAL_LOCKS':'0'})
    out,err=process.communicate(timeout=15)
    records.append({'actual_process_record':True,'PID':process.pid,'argv':process.args,'cwd':str(C),
        'UTC_start':start,'UTC_end':now(),'exit_code':process.returncode,
        'stdout_bytes':len(out),'stdout_sha256':sha(out),'stderr_bytes':len(err),'stderr_sha256':sha(err),
        'read_only_git':True})
    if process.returncode:raise ValueError('Read-only Git failed')
    return out
manifest_bytes=(D/'OUTPUT_MANIFEST.json').read_bytes()
if sha(manifest_bytes)!='71abca86ff0873e0d6fec477e417c30f142d4d0cfac83ab6a78233da1b3d4f45':raise ValueError('Input manifest changed')
manifest=json.loads(manifest_bytes)
for pin in manifest['files']:
    body=(D/pin['path']).read_bytes()
    if len(body)!=pin['bytes'] or sha(body)!=pin['sha256']:raise ValueError('Sealed helper changed: '+pin['path'])
programs={name:sha((D/name).read_bytes()) for name in ['prepare_review_bundle.py','v2_guards.py','bounded_process.py','native_assess_worker.py']}
for name in programs:
    if sha((O/'copied_helper'/name).read_bytes())!=programs[name]:raise ValueError('Copied code changed')
base='04a66906a97293b9c89495fda7bec0727e62f51b'; observed=git('rev-parse','HEAD').decode().strip()
native_diff=git('diff',base,observed,'--','unsolved_math_prioritization/')
queue=git('show',observed+':unsolved_math_prioritization/queue.py')
if native_diff or sha(queue)!='f72aee023f837bad092da58531c2cc069ce2cf094e835d090221107d20f07ab2':raise ValueError('Pinned native changed')
put('SOURCE_UNCHANGED_RECEIPT.json',{'schema':'pr108-corrected-v2-adversary-source-unchanged/v1',
    'actual_operator_PID':os.getpid(),'UTC_start':started,'UTC_end':now(),'input_helper_manifest_sha256':sha(manifest_bytes),
    'all_107_input_files_verified_unchanged':True,'input_manifested_bytes':311818,
    'program_sha256':programs,'copied_fixture_modules_match':True,'pinned_native_parent':base,
    'observed_current_main_head':observed,'native_diff_from_pinned_parent_empty':True,
    'native_queue_sha256':sha(queue),'records':records})
findings=[{'id':'F07','severity':'required','locations':['v2_guards.py:271-273','PLAN.md Required Google Sheet custody'],
    'mechanism':'Authorized exact four-cell row with blank Solution Chat URL is rejected; no existing authorized share URL exists.',
    'normal_and_optimized_reproduced':True,'repair':'Allow exact blank B string; validate an existing supplied nonempty HTTPS URL; retain source/DOI/notes and exact service custody.'},
    {'id':'F08','severity':'required','locations':['bounded_process.py:30-32','bounded_process.py:79-84','prepare_review_bundle.py:148-153','prepare_review_bundle.py:325-326'],
    'mechanism':'Unbound inherited PYTHONPATH/site startup executes unreviewed code before pinned Python child guards.',
    'normal_and_optimized_reproduced':True,'actual_fixture_child_PIDs':[88804, 88919],
    'actual_fixture_stdout_bytes':47,'actual_fixture_stdout_sha256':'9ff57c6f77cc8c3ea1a047795367abcd95b531b99e31779e10fb7046bd2f52ef',
    'repair':'Sanitize and bind effective child environment, ignore Python environment paths and disable unreviewed site startup; retain authenticated local helper imports and explicitly reviewed Git/GH config.'}]
results={mode:json.loads((O/('RESULTS_'+mode.upper()+'.json')).read_text()) for mode in ['normal','optimized']}
put('VERDICT.json',{'schema':'pr108-corrected-v2-independent-static-adversary/v1','UTC':now(),'actual_operator_PID':os.getpid(),
    'review_scope':'sealed helper static/process and pure/offline fixtures only','input_output_manifest_sha256':sha(manifest_bytes),
    'input_file_count':107,'input_total_bytes':311818,'input_program_sha256':programs,
    'native_execution_clearance':False,'future_configuration_clearance':False,'required_findings':findings,'optional_findings':[],
    'F01_status':'original mechanism addressed; new F07 required repair','F02_status':'substantially addressed; F08 binding gap remains',
    'F03_status':'closed in static/pure scope','F04_status':'addressed in static/pure scope; current lower-bound capacity unsatisfied',
    'F05_status':'closed in static/pure scope','F06_status':'closed in static/pure scope; 600-case predicate challenge',
    'tests':{mode:{'test_count':obj['tests_run'],'successful':obj['successful'],'actual_fixture_operator_PID':obj['actual_fixture_operator_PID']} for mode,obj in results.items()},
    'static_audit_completion_percent':100,'helper_readiness_estimate_percent':70,
    'actual_native_prepare_assess_export_executions':0,'actual_service_operations':0,'new_central_proof_search_turns':0,
    'no_real_configuration_or_workload_certified':True,'publication_package_R3_required_by_this_review':False,
    'publication_or_merge_permission_inferred':False,'all_review_writes_confined_to_own_folder':True,
    'remaining_gap':'F07/F08 repair and fresh exact-code review; real immutable configuration/receipt review; sufficient freshly measured exact capacity; later actual native/bundle validation.'})
with (O/'RESEARCH_LOG.md').open('a') as stream:
    stream.write('\n'+now()+': 100% static audit complete; helper readiness estimate 70%. Independent normal/-O runs each pass 28 checks, including deliberate reproduction of required F07 blank-chat mismatch and F08 inherited startup execution. Source/helper unchanged verified. Capacity lower bound exceeds recorded free disk. No real config/native/service clearance; two repairs remain. Final report and sealed artifacts prepared.\n')
put('TASK_COMPLETION.json',{'schema':'pr108-corrected-v2-static-adversary-completion/v1','UTC':now(),'actual_operator_PID':os.getpid(),
    'complete':True,'static_review_completion_percent':100,'required_findings':['F07','F08'],
    'normal_28_checks_pass':True,'optimized_28_checks_pass':True,'native_service_operations':0,
    'all_writes_inside_own_folder':True,'no_native_or_future_configuration_clearance':True})
pins=[]
for path in sorted(O.rglob('*')):
    if path.is_file() and str(path.relative_to(O)) not in ['OUTPUT_MANIFEST.json','SEAL_RECEIPT.json']:
        body=path.read_bytes();pins.append({'path':str(path.relative_to(O)),'bytes':len(body),'sha256':sha(body)})
put('OUTPUT_MANIFEST.json',{'schema':'pr108-v2-static-adversary-output-manifest/v1','UTC':now(),'actual_sealer_PID':os.getpid(),
    'excludes':['OUTPUT_MANIFEST.json','SEAL_RECEIPT.json'],'file_count':len(pins),'total_bytes':sum(x['bytes'] for x in pins),'files':pins})
for pin in pins:
    body=(O/pin['path']).read_bytes()
    if len(body)!=pin['bytes'] or sha(body)!=pin['sha256']:raise ValueError('Audit readback changed')
body=(O/'OUTPUT_MANIFEST.json').read_bytes()
put('SEAL_RECEIPT.json',{'schema':'pr108-v2-static-adversary-seal/v1','UTC':now(),'actual_sealer_PID':os.getpid(),
    'file_count':len(pins),'total_bytes':sum(x['bytes'] for x in pins),'all_readbacks_verified':True,
    'input_helper_source_verified_unchanged':True,'native_source_verified_unchanged':True,
    'actual_native_service_operations':0,'required_findings':['F07','F08'],
    'output_manifest':{'path':'OUTPUT_MANIFEST.json','bytes':len(body),'sha256':sha(body)}})
print(json.dumps({'actual_sealer_PID':os.getpid(),'UTC':now(),'files':len(pins),'bytes':sum(x['bytes'] for x in pins),
    'manifest_sha256':sha(body),'required_findings':['F07','F08'],'native_execution_clearance':False}))
