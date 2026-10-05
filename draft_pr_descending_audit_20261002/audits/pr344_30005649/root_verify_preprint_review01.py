#!/usr/bin/env python3
"""Close the historical adverse review without approving the defective package."""
from pathlib import Path
import datetime,hashlib,json,os,stat,subprocess,sys
A=Path(__file__).resolve().parent;N=A/'preprint_review_01'
OUT=A/'root_preprint_private/review01_root001'
M=N/'OWNED_NAMESPACE_MANIFEST.json'
EXPECTED='d4abe1b7e2fa0f57b9209718338c822fd886084ffadae86bc1446f6fba349d95'
PINS={'REPORT.md':'5d33f04426f08610ee56ca7f1be9657a79a17d1480a73e141de636e02084a2ba',
      'verify_review.py':'152228904f08371996474fd2bb6b19295531f942792b272c06c17896dc8f1e4a',
      'independent_controls.py':'3052195a047927656cbf9a8cf69f6afcb9e8c244e9a5bab8d8fba6c8ef998127',
      'REVIEW_RESULT.json':'312860d175bcd6ff67463a78d56da0f8d32f1db9b5e7e9f71134494daa2ce164',
      'READ_LEDGER.json':'42ccb5c61dd3c7e1ec5f97b8785a3dc73f2e80b97d754b9a404dee145b2c548c',
      'CLOSURE_PLAN.md':'95717e1a8285c083a811d4b182cee78a38491f358d15902224e7c3028ff4fa1d',
      'SOURCE_ONLY_TARGET.md':'44fd7dc04061f5333c8fe9b22845d0643d40358d24c8ef4ef444f875e92f7fed',
      'FIRST_MATHEMATICAL_ASSESSMENT.md':'25cfa18ed889cc066caa8ac18bda166192254f64c225ba4723618620894c905e'}
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def pin(p):
    b=p.read_bytes();return dict(bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),mode=f'{stat.S_IMODE(p.stat().st_mode):04o}')
assert not OUT.exists() and not (A/'ROOT_PREPRINT_REVIEW01_VERIFICATION.json').exists()
assert pin(M)['sha256']==EXPECTED
manifest=json.loads(M.read_bytes());assert manifest['sealed'] is False and manifest['review_verdict']=='REPAIR_REQUIRED'
def inventory():
    files={};dirs={}
    for p in N.rglob('*'):
        assert not p.is_symlink()
        if p.is_file():files[p.relative_to(N).as_posix()]=pin(p)
        elif p.is_dir():dirs[p.relative_to(N).as_posix()]=f'{stat.S_IMODE(p.stat().st_mode):04o}'
    return dict(files=files,directories=dirs,root_mode=f'{stat.S_IMODE(N.stat().st_mode):04o}')
before=inventory()
assert {k:v for k,v in before['files'].items() if k!=M.name}==manifest['files']
assert before['directories']==manifest['directories'] and before['root_mode']==manifest['root_mode']
assert len(manifest['files'])==346 and len(manifest['directories'])==18
assert all(pin(N/name)['sha256']==expected for name,expected in PINS.items())
inputs=json.loads((N/'CANDIDATE_INPUT_MANIFEST.json').read_bytes())['inputs']
assert len(inputs)==6
for e in inputs:
    expected={k:e[k] for k in ('bytes','sha256','mode')}
    assert pin(Path(e['snapshot']))==expected==pin(Path(e['source']))
result=json.loads((N/'REVIEW_RESULT.json').read_bytes())
assert result['verdict']=='REPAIR_REQUIRED' and result['review_complete'] and not result['publication_ready']
assert len(result['blocking_findings'])==1 and result['blocking_findings'][0]['id']=='B1'
assert result['unresolved_mathematical_findings']==[]
OUT.mkdir(parents=True)
receipts=[];results=[]
interpreters=[sys.executable,'/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3']
for i,interpreter in enumerate(interpreters):
    for scope in ('public','full'):
        tag=f'{i}_{scope}';argv=[interpreter,'-B',str(N/'verify_review.py'),'--scope',scope]
        pre=dict(utc=utc(),argv=argv,cwd=str(A),orchestrator=pin(Path(__file__)),input_manifest=pin(M),
            environment_overrides={'PYTHONDONTWRITEBYTECODE':'1','PYTHONHASHSEED':'0'})
        (OUT/(tag+'.preexecution.json')).write_text(json.dumps(pre,indent=2)+'\n')
        r=subprocess.run(argv,cwd=A,capture_output=True,env=dict(os.environ,**pre['environment_overrides']))
        (OUT/(tag+'.stdout')).write_bytes(r.stdout);(OUT/(tag+'.stderr')).write_bytes(r.stderr)
        rec=dict(pre,completed_utc=utc(),exit_status=r.returncode,stdout=pin(OUT/(tag+'.stdout')),stderr=pin(OUT/(tag+'.stderr')))
        (OUT/(tag+'.native_receipt.json')).write_text(json.dumps(rec,indent=2)+'\n');receipts.append(rec)
        assert r.returncode==0 and not r.stderr and inventory()==before
        v=json.loads(r.stdout);results.append(v)
        assert v['review_record_check']=='PASS' and v['review_verdict']=='REPAIR_REQUIRED' and v['publication_ready'] is False
        assert v['namespace_manifest_sha256']==EXPECTED and v['zip_members']==32 and v['owned_namespace_unchanged']
        assert len(v['standalone_control_runs'])==7 and all(x['exit_code']==0 and x['stderr_bytes']==0 for x in v['standalone_control_runs'])
        assert v['submitted_full_run']['exit_code']==(0 if i==0 else 1)
        if scope=='full':assert v['checked_body_pins']==346 and v['historical_native_receipts_checked']==51
for i in (0,2):
    a,b=results[i],results[i+1]
    assert a['standalone_control_runs']==b['standalone_control_runs'] and a['submitted_full_run']==b['submitted_full_run']
for a,b in zip(results[1]['standalone_control_runs'],results[3]['standalone_control_runs']):
    if a['name']!='intrinsic':assert a['stdout_sha256']==b['stdout_sha256']
assert inventory()==before
seal=dict(utc=utc(),status='HISTORICAL_ADVERSE_REVIEW_CLOSED_REPAIR_REQUIRED',
    namespace_manifest_sha256=EXPECTED,namespace_files_including_manifest=347,directory_modes=18,
    namespace_inventory=before,review_verdict='REPAIR_REQUIRED',publication_ready=False,
    mathematics_findings_remaining=0,blocking_findings=['B1'],closure_authority='root after complete scientific/code/ledger/native review and external independent native replay',
    namespace_mutated_by_closure=False,root_native_receipts=receipts)
(A/'ROOT_PREPRINT_REVIEW01_SEAL.json').write_text(json.dumps(seal,indent=2)+'\n')
verification=dict(utc=utc(),status='REVIEW_COMPLETE_PUBLICATION_BLOCKER_RETAINED',
    mandatory_findings=1,unresolved_mathematical_findings=0,findings=result['blocking_findings'],
    sealed_original_input_files=inputs,namespace_manifest_sha256=EXPECTED,
    review_seal_path='ROOT_PREPRINT_REVIEW01_SEAL.json',review_seal_sha256=pin(A/'ROOT_PREPRINT_REVIEW01_SEAL.json')['sha256'],
    full_namespace_and_directory_modes_verified=True,closed_namespace_unchanged=True,
    four_native_public_full_replays_pass=True,historical_native_receipt_count=51,
    system_submitted_full_exit=0,bundled_submitted_full_exit=1,
    original_live_inputs_equal_frozen_copies_before_closure=True,publication_ready=False,
    native_capture_directory=str(OUT),math_percent=100,priority_percent=100,publication_workflow_percent=55)
(A/'ROOT_PREPRINT_REVIEW01_VERIFICATION.json').write_text(json.dumps(verification,indent=2)+'\n')
print(json.dumps(verification,indent=2))
