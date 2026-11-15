#!/usr/bin/env python3
"""Read-only sealed packet closure, retaining exact custom/native statuses."""
from pathlib import Path
import json,hashlib,subprocess,sys
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;P=R.parents[1]
def ck(t,m):
 if not t:raise RuntimeError(m)
def js(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(file,opt=False,args=()):return subprocess.run([sys.executable,'-B']+(['-O'] if opt else [])+[str(R/file),*args],cwd=P,text=True,capture_output=True,timeout=60)
seal=js(R/'FINAL_SEAL.json');manifest=js(R/'FINAL_MANIFEST.json')
ck(sha(R/'FINAL_MANIFEST.json')==seal['manifest_SHA256'],'final manifest binding')
def owned():
 ck({str(p.relative_to(R)) for p in R.rglob('*') if p.is_file()}=={x['path'] for x in manifest['files']}|{'FINAL_MANIFEST.json','FINAL_SEAL.json'},'owned file set changed')
 for x in manifest['files']:
  p=R/x['path'];ck(p.stat().st_size==x['bytes'] and sha(p)==x['SHA256'],'owned bytes '+x['path'])
owned();verdict=js(R/'VERDICT.json')
ck(verdict['assessment']=='FULL_ORDINARY_RATIONAL_LOW_DEGREE_AND_EXACT_ORDER_SEVEN_RESULT_SUPPORTED_WITH_EXPLICIT_GEOMETRIC_IMPORTS','literal custom scientific verdict')
ck(verdict['substantive_mathematical_defect_found'] is False and verdict['exact_remaining_mathematical_gap'] is None,'literal gap fields')
a=run('verify_custody.py');ck(a.returncode==0 and not a.stderr and json.loads(a.stdout)==js(R/'SOURCE_CUSTODY.json'),'complete native/initial/primary custody')
for opt,mode in [(False,'NORMAL'),(True,'OPTIMIZED')]:
 a=run('independent_exact.py',opt);ck(a.returncode==0 and not a.stderr and json.loads(a.stdout)==js(R/('INDEPENDENT_'+mode+'.json')),'independent exact mode reproduction')
 for name in ['degree_two','wheel','symbolic']:
  a=run('replay_native_no_write.py',opt,[name]);ck(a.returncode==0 and not a.stderr,'read-only native execution')
  d=json.loads(a.stdout);ck(d['filesystem_writes']==0,'native no-write guard')
  x=d['output'];y=js(R/('SUPPLIED_'+name.upper()+'_'+mode+'.json'))
  x.pop('utc',None);y.pop('utc',None);ck(x==y,'entire native arithmetic content reproduced')
a=run('semantic_faults.py');ck(a.returncode==0 and not a.stderr and json.loads(a.stdout)==js(R/'SEMANTIC_FAULTS.json'),'semantic faults reproduce')
ck(js(R/'SUPPLIED_DEGREE_TWO_NORMAL.json')['status']=='PASS','native degree-two literal status')
ck(js(R/'SUPPLIED_WHEEL_NORMAL.json')['all_checks_pass'] is True,'native wheel literal status')
ck(js(R/'SUPPLIED_SYMBOLIC_NORMAL.json')['passed'] is True,'native symbolic literal status')
ck(js(R/'CERTIFICATE_COMPARISON.json')[0]['entire_JSON_equal'] is False,'raw wrapper comparison history retained')
ck(js(R/'CERTIFICATE_COMPARISON_SCHEMA_AWARE.json')['assessment']=='ALL_REPLAYED_ARITHMETIC_CONTENT_MATCHES_WITH_NATIVE_WRAPPERS_PRESERVED','schema-aware exact certificate comparison')
owned();a=run('verify_custody.py');ck(a.returncode==0 and not a.stderr,'closure did not mutate sources')
print(json.dumps({'assessment':'SEALED_ANALYTIC115_CUSTODY_AND_EXACT_BOUNDED_REPRODUCTION_SUPPORTED','scientific_assessment':verdict['assessment'],'owned_payloads':len(manifest['files']),'native_total_files':210,'ZIP_regular_occurrences':194,'external_primary_bindings':20,'independent_explicit_checks_each_mode':60,'semantic_fault_sites':5,'semantic_fault_executions':10,'native_arithmetic_replays':6,'native_program_output_file_writes_in_closure':0,'native_statuses':{'degree_two':'PASS','wheel_all_checks_pass':True,'symbolic_passed':True},'final_seal_SHA256':sha(R/'FINAL_SEAL.json'),'manifest_SHA256':sha(R/'FINAL_MANIFEST.json'),'all_verification_read_only':True,'completion_percent':100},indent=2,sort_keys=True))
