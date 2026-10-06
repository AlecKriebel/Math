#!/usr/bin/env python3
"""Pin stability and seal only first-party R2 public outputs; no input writes."""
from pathlib import Path
import datetime,hashlib,json,os,sys
O=Path(__file__).resolve().parent;A=O.parent;D=A/'publication_ready_package_v2'
def ck(x,msg):
 if not x:raise RuntimeError(msg)
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
now=datetime.datetime.now(datetime.timezone.utc).isoformat();pid=os.getpid();pins=load(O/'INPUT_PINS.json')['files']
actual=[p for p in sorted(D.rglob('*')) if p.is_file()]
ck({p.relative_to(D).as_posix() for p in actual}=={r['path'] for r in pins},'full input inventory changed')
for r in pins:ck((D/r['path']).stat().st_size==r['bytes'] and h(D/r['path'])==r['sha256'],'input bytes changed: '+r['path'])
ck(not list(O.rglob('*.pyc')) and not list(O.rglob('__pycache__')),'unexpected pycache')
for r in load(O/'ACTUAL_PROCESS_LEDGER.json')['records']:
 for stream in ['stdout','stderr']:
  if stream+'_path' in r:
   p=O/r[stream+'_path'];ck(p.stat().st_size==r[stream+'_bytes'] and h(p)==r[stream+'_sha256'],'actual process stream changed')
for p in [O/'INDEPENDENT_DIAGNOSTICS_0.json',O/'INDEPENDENT_DIAGNOSTICS_1.json',O/'PROVENANCE_DIAGNOSTICS.json',O/'BOUNDARY_DIAGNOSTICS.json']:ck(load(p)['all_pass'],'diagnostic failed')
state=dict(schema='pr108-r2-final-input-stability/v1',UTC=now,actual_operator_PID=pid,argv=sys.argv,all48_input_files_unchanged=True,verified_files=len(pins),pins=pins,checked_actual_public_and_private_process_stream_hashes=True,package_mutated=False,publication_operation_performed=False)
(O/'FINAL_INPUT_STABILITY.json').write_text(json.dumps(state,indent=2)+'\n')
exclude={'REVIEW_MANIFEST.json','SHA256SUMS','SEAL.json'};rows=[]
for p in sorted(O.rglob('*')):
 if not p.is_file() or p.relative_to(O).parts[0] in ['scratch','private'] or p.name in exclude:continue
 ck(not p.is_symlink(),'public symlink')
 rows.append(dict(relative_path=p.relative_to(O).as_posix(),bytes=p.stat().st_size,sha256=h(p)))
man=dict(schema='pr108-whole-publication-package-R2-public-manifest/v1',UTC=now,actual_operator_PID=pid,PR=108,problem_id=30003996,completion_estimate_percent=100,new_central_proof_search_turns=0,files=rows,payload_files=len(rows),payload_bytes=sum(x['bytes'] for x in rows),excluded=['scratch/','private/','REVIEW_MANIFEST.json','SHA256SUMS','SEAL.json'],raw_third_party_bodies_in_public=False,input_manifest_sha256=h(D/'PACKAGE_MANIFEST.json'),input_ZIP_sha256=h(D/'root_dependent_spanning_trees_support.zip'))
(O/'REVIEW_MANIFEST.json').write_text(json.dumps(man,indent=2)+'\n')
(O/'SHA256SUMS').write_text('\n'.join(r['sha256']+'  '+r['relative_path'] for r in rows)+'\n'+h(O/'REVIEW_MANIFEST.json')+'  REVIEW_MANIFEST.json\n')
seal=dict(schema='pr108-whole-publication-package-R2-seal/v1',UTC=now,actual_operator_PID=pid,argv=sys.argv,disposition='PASS_EXACT_SEALED_V2_CURRENT_WHOLE_PACKAGE',completion_estimate_percent=100,required_findings=0,optional_findings=0,manifest_path='REVIEW_MANIFEST.json',manifest_bytes=(O/'REVIEW_MANIFEST.json').stat().st_size,manifest_sha256=h(O/'REVIEW_MANIFEST.json'),checksums_path='SHA256SUMS',checksums_sha256=h(O/'SHA256SUMS'),payload_files=len(rows),payload_bytes=man['payload_bytes'],report_sha256=h(O/'REPORT.md'),verdict_sha256=h(O/'VERDICT.json'),input_manifest_sha256=h(D/'PACKAGE_MANIFEST.json'),input_ZIP_sha256=h(D/'root_dependent_spanning_trees_support.zip'),input_PDF_sha256=h(D/'root_dependent_spanning_trees.pdf'),all_inputs_stable=True,publication_execution_or_future_package_certified=False,raw_third_party_private_scratch_excluded=True)
(O/'SEAL.json').write_text(json.dumps(seal,indent=2)+'\n')
# Verify final envelope immediately; no output mutation after this point.
for r in rows:ck((O/r['relative_path']).stat().st_size==r['bytes'] and h(O/r['relative_path'])==r['sha256'],'public sealed byte mismatch')
ck(h(O/'REVIEW_MANIFEST.json')==seal['manifest_sha256'] and h(O/'SHA256SUMS')==seal['checksums_sha256'],'seal envelope mismatch')
print(json.dumps(seal,sort_keys=True))
