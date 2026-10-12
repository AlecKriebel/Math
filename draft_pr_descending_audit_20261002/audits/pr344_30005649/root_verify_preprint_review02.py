#!/usr/bin/env python3
"""Externally close historical v03 adverse review; never confer publishing clearance."""
from pathlib import Path
import datetime,hashlib,json,os,stat,subprocess,sys
A=Path(__file__).resolve().parent;N=A/'preprint_review_02';M=N/'FINAL_MANIFEST.json'
OUT=A/'root_preprint_private/review02_root001'
EXPECTED='45c5859aa380724e8155e8ec8eb8662f3add90d4ffc3867e2a4ee990d839d048'
PINS={'REVIEW_REPORT.md':'a03b6e7cad6ed56295a9cdbae564b25ed7aa4dec3dc7110052067c3b416a6338',
'verify_review.py':'39be91c74c5fc76514ec196777242d60fdbeec8ba6501eea14e86fc421e84603',
'SOURCE_READING_LEDGER.json':'c50acd10dce1805b92504d079bd8a82536018eb86fa9e0026fed01673c00d9de',
'REVIEW_STATUS.json':'0999d86e7a66846ee0c2a44cee9ef421fb1b723e899ae7500e57c1c64b39cfbd',
'PROVENANCE.md':'0cc5275260da6057b1f6bdedcae2dcca59c73699a4a5769a022a52bb8c007117',
'ROOT_CLOSURE_PLAN.md':'44b7e38ec5ff0f1c9f21a5b73a814681b1da4e913cc017fe58b50bde94e1ab41',
'freezes/01_SOURCE_ONLY.md':'87c348ba92da7ccb772b1a16f845e98e1334f383ee474cb10ade9fd788a1507a',
'freezes/02_FIRST_MATHEMATICS.md':'cb7f9b78d0cbdb5b20a1cab9d7d1e3f9afddc389616c1469b691a802c7aaabda',
'freezes/03_FORMULA_COUNTEREXAMPLE.md':'9556da0815db9e26ed3c95f19b23e0ca37b271a63222e1e1b75938c8f0e27c9b',
'freezes/TIMESTAMP_CORRECTION.json':'fef0d3947d3b5d534a143480f821f538fafbf438de10923c465ccdc4e66026ea'}
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def pin(p):
 b=p.read_bytes();return dict(bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),mode=format(stat.S_IMODE(p.stat().st_mode),'04o'))
def inventory():
 files={};dirs={}
 for p in N.rglob('*'):
  assert not p.is_symlink()
  if p.is_file():files[p.relative_to(N).as_posix()]=pin(p)
  elif p.is_dir():dirs[p.relative_to(N).as_posix()]=format(stat.S_IMODE(p.stat().st_mode),'04o')
 return dict(files=files,directories=dirs,root_mode=format(stat.S_IMODE(N.stat().st_mode),'04o'))
assert not OUT.exists() and not (A/'ROOT_PREPRINT_REVIEW02_SEAL.json').exists()
assert pin(M)['sha256']==EXPECTED
assert all(pin(N/n)['sha256']==s for n,s in PINS.items())
manifest=json.loads(M.read_text());assert manifest['unsealed'] and manifest['verdict']=='NEEDS_REPAIR' and manifest['self_exclusion']==['FINAL_MANIFEST.json']
before=inventory();entries={'.':dict(type='directory',mode=before['root_mode'])}
entries.update({n:dict(type='file',**v) for n,v in before['files'].items() if n!=M.name})
entries.update({n:dict(type='directory',mode=v) for n,v in before['directories'].items()})
assert entries==manifest['entries'] and len(before['files'])==405 and len(before['directories'])==25
status=json.loads((N/'REVIEW_STATUS.json').read_text())
assert status['review_complete'] and status['package_verdict']=='NEEDS_REPAIR' and status['mandatory_finding_ids']==['F01']
assert status['main_theorem']==status['classical_mechanism']=='VERIFIED_WITH_CLASSICAL_INPUTS'
inputs=json.loads((N/'inputs/PINS.json').read_text());assert len(inputs)==6
for e in inputs:
 expected={k:e[k] for k in ('bytes','sha256','mode')}
 assert pin(N/'inputs'/e['name'])==expected==pin(A/'preprint'/e['name'])
root_evidence=json.loads((A/'root_preprint_private/formula_falsification_001/SUMMARY.json').read_text())
assert root_evidence['status']=='ROOT_INDEPENDENT_EXACT_COUNTEREXAMPLE_REPRODUCED' and root_evidence['supplementary_generic_helper_repair_required']
OUT.mkdir();receipts=[]
for i,exe in enumerate([sys.executable,'/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3']):
 for scope in ('public','full'):
  tag=str(i)+'_'+scope;argv=[exe,'-B',str(N/'verify_review.py'),'--scope',scope]
  pre=dict(utc=utc(),argv=argv,cwd=str(A),controller=pin(Path(__file__)),manifest=pin(M),environment_overrides={'PYTHONDONTWRITEBYTECODE':'1','PYTHONHASHSEED':'0'})
  (OUT/(tag+'.preexecution.json')).write_text(json.dumps(pre,indent=2)+'\n')
  r=subprocess.run(argv,cwd=A,capture_output=True,env=dict(os.environ,**pre['environment_overrides']))
  (OUT/(tag+'.stdout')).write_bytes(r.stdout);(OUT/(tag+'.stderr')).write_bytes(r.stderr)
  rec=dict(pre,end_utc=utc(),exit_status=r.returncode,stdout=pin(OUT/(tag+'.stdout')),stderr=pin(OUT/(tag+'.stderr')))
  (OUT/(tag+'.native_receipt.json')).write_text(json.dumps(rec,indent=2)+'\n');receipts.append(rec)
  assert r.returncode==0 and not r.stderr and inventory()==before
  v=json.loads(r.stdout);assert v['integrity_status']=='PASS' and v['package_verdict']=='NEEDS_REPAIR' and v['mandatory_finding_ids']==['F01']
  assert v['owned_namespace_unchanged'] and v['frozen_zip_members']==32 and v['six_inputs']==6
  assert len(v['fresh_native_replays'])==(8 if scope=='full' else 0)
assert inventory()==before
seal=dict(utc=utc(),status='HISTORICAL_ADVERSE_REVIEW_CLOSED_NEEDS_REPAIR',namespace_manifest_sha256=EXPECTED,namespace_inventory=before,namespace_files_including_manifest=405,directory_modes_excluding_root=25,main_theorem_valid=True,classical_mechanism_valid=True,mandatory_findings=['F01'],publication_ready=False,namespace_mutated_by_closure=False,closure_authority='root after full report/ledger/provenance/final-code/native-negative read, independent formula reproduction, and external native public/full replay on two runtimes',root_native_receipts=receipts)
f=A/'ROOT_PREPRINT_REVIEW02_SEAL.json';f.write_text(json.dumps(seal,indent=2)+'\n')
verification=dict(utc=utc(),status='REVIEW_COMPLETE_SUBSTANTIVE_HELPER_BLOCKER_RETAINED',historical_revision='03',findings=status['mandatory_findings'],main_theorem_valid=True,classical_mechanism_valid=True,generic_helper_valid=False,sealed_original_input_files=inputs,namespace_manifest_sha256=EXPECTED,review_seal_sha256=pin(f)['sha256'],historical_native_receipt_count=28,four_native_public_full_replays_pass=True,closed_namespace_unchanged=True,original_live_inputs_equal_frozen_before_closure=True,requires_substantive_public_derivative_repair=True,requires_new_full_preprint_reviewer=True,publication_ready=False,math_percent=100,priority_percent=100,workflow_percent=60,native_capture_directory=str(OUT))
(A/'ROOT_PREPRINT_REVIEW02_VERIFICATION.json').write_text(json.dumps(verification,indent=2)+'\n')
print(json.dumps(verification,indent=2))
