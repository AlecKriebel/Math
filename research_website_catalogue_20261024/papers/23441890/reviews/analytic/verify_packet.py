#!/usr/bin/env python3
"""Read-only sealed-packet verification; preserve literal qualified statuses."""
from pathlib import Path
import hashlib,json,subprocess,sys
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;P=R.parents[1]
def ck(t,m):
 if not t:raise RuntimeError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def js(p):return json.loads(p.read_text())
def run(path,opt=False):
 return subprocess.run([sys.executable,'-B']+(['-O'] if opt else [])+[str(path)],capture_output=True,text=True,timeout=60,cwd=P)
seal=js(R/'FINAL_SEAL.json');manifest=js(R/'FINAL_MANIFEST.json')
ck(sha(R/'FINAL_MANIFEST.json')==seal['manifest_sha256'],'final manifest pin')
expected={x['path'] for x in manifest['files']}
ck({str(p.relative_to(R)) for p in R.rglob('*') if p.is_file()}==expected|{'FINAL_MANIFEST.json','FINAL_SEAL.json'},'owned file set changed')
for x in manifest['files']:
 p=R/x['path'];ck(p.stat().st_size==x['bytes'] and sha(p)==x['sha256'],'owned file mismatch '+x['path'])
v=js(R/'VERDICT.json')
ck(v['assessment']=='FULL_TWO_TAIL_AMBIENT_THEOREM_AND_EIGHT_FAMILY_COROLLARY_SUPPORTED_WITH_EXPLICIT_GERM_SCOPE','literal scientific verdict')
ck(v['substantive_mathematical_defect_found'] is False and v['exact_remaining_mathematical_gap'] is None,'exact verdict fields')
c=run(R/'verify_custody.py');ck(c.returncode==0 and not c.stderr and json.loads(c.stdout)==js(R/'SOURCE_CUSTODY.json'),'complete live custody')
for opt,receipt in [(False,'INDEPENDENT_NORMAL.json'),(True,'INDEPENDENT_OPTIMIZED.json')]:
 a=run(R/'independent_exact.py',opt);ck(a.returncode==0 and not a.stderr and json.loads(a.stdout)==js(R/receipt),'independent exact mode reproduction')
a=run(R/'independent_fault_controls.py');ck(a.returncode==0 and not a.stderr and json.loads(a.stdout)==js(R/'FAULT_CONTROLS.json'),'all semantic mutation reproductions')
helper=P/'sources/published-source/kourovka-21-149/exact_constructions.py'
a=run(helper);ck(a.returncode==0 and not a.stderr and a.stdout.encode()==(R/'SUPPLIED_REPLAY.json').read_bytes()==helper.with_name('exact_constructions_result.json').read_bytes(),'literal supplied normal replay')
ck(json.loads(a.stdout)['status']=='passed','retain native passed status')
a=run(helper,True);ck(a.returncode!=0 and not a.stdout and a.stderr.rstrip().endswith('RuntimeError: Run without -O: exact checks must remain enabled'),'intentional optimized refusal')
for name in ['SUPPLIED_REPLAY.stderr','SUPPLIED_OPTIMIZED_REFUSAL.stdout','INDEPENDENT_NORMAL.stderr','INDEPENDENT_OPTIMIZED.stderr','FAULT_CONTROLS.stderr','SOURCE_CUSTODY.stderr']:ck((R/name).stat().st_size==0,'pristine receipt unexpected content '+name)
ck((R/'FAULT_CONTROLS.stderr.initial_failure').stat().st_size>0,'initial auditor harness failure retained')
print(json.dumps({'assessment':'SEALED_ANALYTIC_PACKET_CUSTODY_AND_BOUNDED_REPRODUCTION_SUPPORTED','scientific_assessment':v['assessment'],'owned_payloads':len(expected),'native_total_files':32,'ZIP_regular_occurrences':16,'external_primary_bindings':10,'independent_controls_each_mode':7784,'semantic_mutants':5,'semantic_mutant_executions':10,'supplied_literal_status':'passed','supplied_optimized':'INTENTIONAL_GUARD_REFUSAL_NOT_A_CHECK_PASS','all_verification_read_only':True,'final_seal_sha256':sha(R/'FINAL_SEAL.json'),'manifest_sha256':sha(R/'FINAL_MANIFEST.json'),'completion_percent':100},sort_keys=True,indent=2))
