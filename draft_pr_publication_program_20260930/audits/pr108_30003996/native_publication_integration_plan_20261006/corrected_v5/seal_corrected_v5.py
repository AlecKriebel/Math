"""Seal only the current own-folder nonexecuted V5 draft; no native/Git/service action."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import datetime,json,os,shutil,stat
import v3_guards as g
D=Path(__file__).resolve().parent
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def write(name,obj):(D/name).write_bytes(g.canonical(obj))
g.validate_python_startup(os.environ)
g.require(not (D/'OUTPUT_MANIFEST.json').exists() and not (D/'SEAL_RECEIPT.json').exists(),'V5 already sealed')
prior=g.loads((D/'PREDECESSOR_UNCHANGED_INPUT_PINS.json').read_bytes());counts={}
for item in prior['files']:
    p=Path(item['path']);g.regular(p);data=p.read_bytes()
    g.require(len(data)==item['bytes'] and g.sha(data)==item['sha256'],'Predecessor changed at final seal')
    counts[item['group']]=counts.get(item['group'],0)+1
read=g.loads((D/'READ_SCOPE_MANIFEST.json').read_bytes())
for item in read['files']:
    chosen=item.get('retained_byte_identical_copy',item);p=Path(chosen['path']);g.regular(p);data=p.read_bytes()
    g.require(len(data)==item['bytes'] and g.sha(data)==item['sha256'],'Actual read pin body unverified')
for mode in ['NORMAL','OPTIMIZED']:
    result=g.loads((D/(mode+'_FIXTURE_RESULTS.json')).read_bytes())
    g.require(result['all_passed'] is True and result['tests']==35 and result['exit_code']==0,'Final fixtures not successful')
    for field in ['stdout','stderr']:
        p=Path(result[field]['path']);data=p.read_bytes();g.require(len(data)==result[field]['bytes'] and g.sha(data)==result[field]['sha256'],'Test output body differs')
for mode in ['normal','optimized']:
    fixture=D/'fixture_startup'/mode
    g.require(not (fixture/'STARTUP_INJECTION_SENTINEL_MUST_BE_ABSENT').exists(),'Startup injection sentinel exists')
    result=g.loads((fixture/'ABSENT_SENTINEL_RESULT.json').read_bytes())
    g.require(result['sentinel_present'] is False and result['native_prepare_assess_export_calls']==0,'Startup regression not passed')
core={name:{'bytes':(D/name).stat().st_size,'sha256':g.sha((D/name).read_bytes())} for name in g.PROGRAMS}
ledger=g.loads((D/'FIELD_SPECIFIC_CORRECTION_LEDGER.json').read_bytes())
g.require({Path(p['path']).name:p['sha256'] for p in ledger['program_pins']}=={k:v['sha256'] for k,v in core.items()},'Template/ledger core pins stale')
g.require([x['finding'] for x in ledger['corrections']]==['F01','F02','F03','F04','F05','F06','F07','F08','F09','F10'],'Correction ledger incomplete')
for name,function in [('CONFIG_TEMPLATE_DO_NOT_RUN.json',g.validate_thin_config),('EXECUTION_INPUTS_TEMPLATE_DO_NOT_RUN.json',lambda o:g.validate_execution_manifest(o,g.canonical(o)))]:
    try:function(g.loads((D/name).read_bytes()))
    except ValueError:pass
    else:raise ValueError('Inert template accepted at seal')
diff=g.loads((D/'SOURCE_DIFF_MANIFEST.json').read_bytes())
for item in diff['programs']:
    for label in ['V4','V5']:
        pin=item[label];data=Path(pin['path']).read_bytes();g.require(len(data)==pin['bytes'] and g.sha(data)==pin['sha256'],'Full source diff pin changed')
data=(D/diff['diff']['path']).read_bytes();g.require(len(data)==diff['diff']['bytes'] and g.sha(data)==diff['diff']['sha256'],'Full source diff body changed')
g.require(g.loads((D/'WORKER_CONTROL_CONTRACT.json').read_bytes())['runtime_control_constructed'] is False,'Contract is not inert')
utc=now();free=shutil.disk_usage(D).free
write('CORE_FAMILY_MANIFEST.json',{'schema':'pr108-corrected-v5-core-family/v1','UTC':utc,'draft_only':True,'program_files':core,
    'code_family_sha256':g.sha(g.canonical(core)),'joint_V5_actual_inputs_review_clearance':False})
with (D/'RESEARCH_LOG.md').open('a') as file:
    file.write('\n'+utc+' — Sealed corrected_v5 draft100% for exact-code adversarial review, not native commissioning. Normal/optimized35/35 custody verified; every read input body and predecessor pin verified. V1/V2/V3/V4 unchanged. Final native prepare/assess/export/install count0, service calls0, Git commands0, central proof turns0. Real config/capacity/gates and later candidate/DIFF/readbacks remain future work.\n')
entries=[]
for p in sorted(D.rglob('*')):
    g.require(not p.is_symlink(),'Symlink in draft seal')
    if not p.is_file():continue
    data=p.read_bytes();entries.append({'relative_path':str(p.relative_to(D)),'bytes':len(data),'sha256':g.sha(data),'mode':format(stat.S_IMODE(p.stat().st_mode),'04o')})
write('OUTPUT_MANIFEST.json',{'schema':'pr108-corrected-v5-allfiles-output-manifest/v1','UTC':utc,'actual_sealer_PID':os.getpid(),
    'scope':'All current corrected_v3 files except this output manifest and its subsequent noncircular seal receipt',
    'files':entries,'file_count':len(entries),'total_bytes':sum(x['bytes'] for x in entries),'core_family':core,
    'all_F01_through_F10_addressed_in_draft':True,'native_Git_service_executions':0,'new_central_proof_search_turns':0})
manifest=(D/'OUTPUT_MANIFEST.json').read_bytes()
write('SEAL_RECEIPT.json',{'schema':'pr108-corrected-v5-actual-seal-receipt/v1','UTC':utc,'actual_sealer_PID':os.getpid(),'sealed':True,
    'output_manifest':{'path':str(D/'OUTPUT_MANIFEST.json'),'bytes':len(manifest),'sha256':g.sha(manifest)},
    'manifested_file_count':len(entries),'manifested_bytes':sum(x['bytes'] for x in entries),'allfiles_including_manifest_and_receipt':len(entries)+2,
    'core_family':core,'core_family_sha256':g.sha(g.canonical(core)),'verified_predecessor_counts':counts,
    'actual_tests_per_mode':35,'normal_actual_PID':g.loads((D/'NORMAL_FIXTURE_RESULTS.json').read_bytes())['actual_PID'],
    'optimized_actual_PID':g.loads((D/'OPTIMIZED_FIXTURE_RESULTS.json').read_bytes())['actual_PID'],
    'free_bytes_snapshot':free,'capacity_clearance':False,'actual_runtime_configuration_prepared':False,
    'native_prepare_assess_export_install_executions':0,'service_calls':0,'Git_commands':0,'new_central_proof_search_turns':0,
    'conventional_peer_review_or_joint_V5_actual_inputs_review_clearance_claimed':False,'existing_combined_source_and_actual_inputs_review_still_required':True,'actual_private_config_or_credential_bodies_read_or_copied':False,'actual_frozen_inputs_modified_by_this_effort':False,'separate_duplicate_source_review_stage_added':False,
    'memory_limit_certification':'Darwin memory advisory; no hard memory bound or native workload success claimed',
    'contact_or_outreach_prepared_or_made':False})
# Read back all manifested bytes and exact current file set after sealing.
for item in entries:
    data=(D/item['relative_path']).read_bytes();g.require(len(data)==item['bytes'] and g.sha(data)==item['sha256'],'Output readback mismatch')
g.require({str(x.relative_to(D)) for x in D.rglob('*') if x.is_file()}=={x['relative_path'] for x in entries}|{'OUTPUT_MANIFEST.json','SEAL_RECEIPT.json'},'Unsealed extra output')
print(json.dumps({'sealed':True,'UTC':utc,'actual_sealer_PID':os.getpid(),'output_manifest_sha256':g.sha(manifest),
    'manifested_files':len(entries),'manifested_bytes':sum(x['bytes'] for x in entries),'allfiles_count':len(entries)+2,
    'core_family_sha256':g.sha(g.canonical(core)),'core_family':core,'predecessor_counts':counts,'free_bytes_snapshot':free,'native_calls':0}))
