#!/usr/bin/env python3
"""Read-only closure verifier. No network, source execution or file writes.

An unsealed preflight is available only to create the recorded receipt; ordinary
invocation requires the final seal. Mathematical truth is not inferred from hashes.
"""
from pathlib import Path
import hashlib,json,subprocess,sys

R=Path(__file__).resolve().parent
B=R.parents[1]
S=B/'sources'
checks=0
def check(p,label):
    global checks
    checks+=1
    if not p:raise RuntimeError(label)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def obj(p):return json.loads(p.read_text())

for mname in ['INPUT_MANIFEST.json','OWNED_MANIFEST.json']:
    for f in obj(R/mname)['files']:
        p=Path(f['path']) if mname.startswith('INPUT') else R/f['path']
        check(p.is_file() and p.stat().st_size==f['bytes'] and sha(p)==f['sha256'],mname+': '+f['path'])
excluded={'OWNED_MANIFEST.json','SEAL.json','verification_output.json'}
actual={str(p.relative_to(R)) for p in R.rglob('*') if p.is_file() and str(p.relative_to(R)) not in excluded}
listed={f['path'] for f in obj(R/'OWNED_MANIFEST.json')['files']}
check(actual==listed,'all owned payloads inventoried, no extra or missing files')
check(sha(S/'SOURCE_READY.json')=='61f1a6961c0255fd94bc9789fb468b7baded2a37f988ef0b3000a272306b77cf','source-ready pin')
check(sha(R/'INITIAL_RECONSTRUCTION.md')==obj(R/'INITIAL_SEAL.json')['reconstruction_sha256']=='569e96c8adf87cd65821692d2d06e0687f20e5617f1ce26a0a6d7f8ec7db71e6','initial independent reconstruction seal')
check(obj(R/'INITIAL_SEAL.json')['primary_bodies_or_deposited_programs_or_opinions_read'] is False,'initial exposure boundary')

# This historical helper was personally inspected: only JSON/hash/native MD5,
# ZIP CRC/path/type checks; no network, scientific code or mutation.
old=B/'reviews/source_custody/verify_source_custody.py'
p=subprocess.run([sys.executable,'-B',str(old)],capture_output=True,text=True,timeout=30)
check(p.returncode==0,'unchanged acquisition closure helper')
custody=json.loads(p.stdout)
check(custody['status']=='PASS' and custody['regular_members']==16 and custody['all_original_source_bytes_unchanged'],'native custody all sixteen payloads')

receipts=obj(R/'EXECUTION_RECEIPTS.json')['executions']
check([e['tag'] for e in receipts]==['native-normal','native-optimized-control','independent-normal','independent-optimized'],'all declared execution modes')
for e in receipts:
    check(sha(Path(e['command'][-1]))==e['program_sha256'],'executed program identity '+e['tag'])
native=obj(R/'native-normal.stdout.txt')
check(native==obj(S/'published-source/kourovka-21-149/exact_constructions_result.json'),'whole native output equals deposited object')
check(receipts[0]['exit_code']==0 and native['status']=='passed','normal native success')
check(receipts[1]['exit_code']!=0 and 'Run without -O' in (R/'native-optimized-control.stderr.txt').read_text(),'optimized native refusal control')
ind=obj(R/'independent-normal.stdout.txt')
check(ind==obj(R/'independent-optimized.stdout.txt') and ind['status']=='passed','whole independent outputs equal under optimization')
check(ind['checks']=={'tuple_maps_checked_as_whole_PL_functions':320,'tail_local_nontriviality_and_first_germs':48,'whole_function_automorphism_products':1,'orientation_tail_pairs':69,'shift_countermodel_exact_knot_cases':132},'bounded independent check scope')
check(receipts[2]['exit_code']==receipts[3]['exit_code']==0,'independent exit status')
lean=R/'cache/primary/Problem_21_149.complete.lean'
z=lean.read_bytes()
check(len(z)==38674 and sha(lean)=='4a69f3e9d739fc1119d5fbf561fc4ca63c064bcdeece6766ff987eabcd8c5655','complete pinned Lean exact UTF8 bytes')
check(hashlib.sha1(b'blob '+str(len(z)).encode()+b'\0'+z).hexdigest()=='16171b31d31c07ba433fa19b73408d515fc9eebb','connector Git blob identity')
for rec in obj(R/'cache/primary/HISTORICAL_NOTEBOOK_CACHE_RECEIPTS.json'):
    d=Path(rec['destination']);check(sha(d)==rec['sha256']==rec['deposited_source_native_manifest_object']['sha256'],'exact historical Notebook cache pin')
verdict=obj(R/'VERDICT.json')
check(verdict['completion_estimate_percent']==100 and not verdict['substantive_mathematical_defect_found'],'literal recorded verdict')
check(not verdict['sibling_scientific_findings_read'] and not verdict['sent_scientific_findings_before_root_gate'],'independence disposition')

sealed='--unsealed-preflight' not in sys.argv
if sealed:
    seal=obj(R/'SEAL.json')
    for name,key in [('INPUT_MANIFEST.json','input_manifest_sha256'),('OWNED_MANIFEST.json','owned_manifest_sha256'),('REPORT.md','report_sha256'),('VERDICT.json','verdict_sha256'),('verify_read_only.py','read_only_verifier_sha256'),('verification_output.json','verification_output_sha256')]:
        check(sha(R/name)==seal[key],'final seal '+name)
    check(seal['source_ready_sha256']==sha(S/'SOURCE_READY.json') and seal['completion_estimate_percent']==100,'source binding and completion seal')
print(json.dumps({'status':'PASS','record_id':23441890,'mode':'sealed' if sealed else 'unsealed preflight','scope_closure_checks':checks,'inherited_native_custody_checks':custody['custody_checks'],'all_original_source_bytes_unchanged':True,'read_only':True,'mathematical_limitation':'Checks custody and recorded evidence, not a formal proof of the theorem.'},indent=2))
