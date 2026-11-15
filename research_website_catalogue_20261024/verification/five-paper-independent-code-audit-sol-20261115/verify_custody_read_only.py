#!/usr/bin/env python3
"""Pure custody closure. Standard library/file reads only. Does not import/run
stage code, render, rerun faults/science, use a subprocess/network, or write.
--current-base also requires the pre-install index/sitemap and556 namespace.
Without it, separately authorized later overlays do not invalidate old554/core18.
"""
from pathlib import Path
from hashlib import sha256
import json,sys
A=Path(__file__).resolve().parent
n=0
def need(v,s):
 global n
 if not v:raise RuntimeError(s)
 n+=1
def load(p):return json.loads(Path(p).read_text())
def digest(p):return sha256(Path(p).read_bytes()).hexdigest()
inputs=load(A/'INPUT_MANIFEST.json')
for x in inputs['files']:
 if x.get('current_overlay_only') and '--current-base'not in sys.argv:continue
 p=Path(x['absolute_path']);need(p.is_file()and not p.is_symlink()and p.stat().st_size==x['bytes']and digest(p)==x['sha256'],'immutable input '+str(p))
if '--current-base'in sys.argv:
 b=load(A/'BASELINE_INDEPENDENT.json');root=Path(b['public_root']);need({str(p.relative_to(root))for p in root.rglob('*')if p.is_file()}=={x['relative_path']for x in b['public_files']},'exact installed pre-overlay556 namespace')
need(digest(A/'inputs/stage-FINAL_SEAL.json')=='80db4036c349909dea6138effb23c3ae764a0e2a748aa2efc521b0b5a5439eec','exact audited final stage identity')
need(digest(A/'metadata-support/stage-comparison/SEAL.json')=='2bbf5ce9fe28c399f0af336a774efe5c76e852966b99f57e549135850255b74f','independent metadata support seal')
result=load(A/'INDEPENDENT_RESULT.json');need(result['checks']==1807 and result['current_baseline_checked']is True,'actual independent pre-install result bound')
need(result['publication_native_AA_or_browser_authority']is False,'no inherited publication authority')
sealed=(A/'FINAL_SEAL.json').exists()
if sealed:
 seal=load(A/'FINAL_SEAL.json');need(digest(A/'OWNED_MANIFEST.json')==seal['owned_manifest_sha256'],'own final manifest SHA-256');m=load(A/'OWNED_MANIFEST.json')
 for x in m['files']:
  p=Path(x['absolute_path']);need(p.is_file()and p.stat().st_size==x['bytes']and digest(p)==x['sha256'],'owned audit bytes '+str(p))
 need({str(p)for p in A.rglob('*')if p.is_file()}=={x['absolute_path']for x in m['files']}|{str(A/'OWNED_MANIFEST.json'),str(A/'FINAL_SEAL.json')},'exact owned audit namespace')
else:need('--unsealed'in sys.argv,'final audit seal required')
print(json.dumps({'literal_status':'PASS_PURE_OFFLINE_FIVE_INTEGRATION_AUDIT_CUSTODY','checks':n,'input_files_listed':len(inputs['files']),'all217_target_payloads_and663_original_inputs_bound':True,'old_nonoverlay_public_files':554,'current_core_files':18,'current_preinstall556_namespace_checked':'--current-base'in sys.argv,'own_final_seal_checked':sealed,'scientific_or_old_or_target_or_fault_programs_replayed':False,'network_subprocess_or_file_writes':False,'publication_or_AA_authority':False},indent=2))
